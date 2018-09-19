# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.models import User,Permission
from django.contrib.auth.hashers import check_password
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.views.defaults import page_not_found
from datetime import datetime
from decimal import *
from SIGPAd.reporte import *
from SIGPAd.reporteDespido import *
from inventario.reporteCompra import *
import openpyxl
from django.core import serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType
from SIGPAd.models import *
from django.db import IntegrityError
from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import UpdateView, CreateView
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import json
from .kardex import nuevoKardex



# Create your views here.
##No somos muy ordenados asique aqui vamos a empezar con el codigo del Sprint 2

#Vistas vendedores.
@permission_required('SIGPAd.view_seller')
def  indexVendedor(request):
	user = request.user
	if user.is_authenticated():
		if user.is_superuser:
			return render(request,'AdministradorTemplates/adminIndex.html',{})
		else:
			return render(request,'VendedorTemplates/vendedorIndex.html',{})			
	return render_to_response('VendedorTemplates/vendedorIndex.html')


@permission_required('SIGPAd.view_seller')
def registrarCategoria(request):
	error = ''
	exito = ''
	if request.method=='POST':
		action = request.POST.get('action')
		if action=='insert':
			codigo = request.POST.get('codigo',None)
			nombre = request.POST.get('nombre',None)
			descripcion = request.POST.get('descripcion',None)
			if codigo!=None and nombre !=None and descripcion !=None :
				try:
					categoria = Categoria()
					categoria.codigo=codigo
					categoria.nombre=nombre
					categoria.descripcion=descripcion
					categoria.save()
					exito = 'Guardada con exito'
				except Exception as e:
					print(e.message)
					if 'column nombre is not unique' in e.message:
						error='El nombre se repite, intente nuevamente'
					if 'column codigo is not unique' in e.message:
						error='El código que esta insertando ya esta ocupado'
	categorias = Categoria.objects.all()
	consulta = request.GET.get('consulta')
	if consulta:
		categorias = categorias.filter(
			Q(nombre__icontains = consulta)|
			Q(codigo__icontains = consulta)
			).distinct()
	paginator = Paginator(categorias, 7)
	parametros = request.GET.copy()
	if parametros.has_key('page'):
		del parametros['page']
	
	page = request.GET.get('page')
	try:
		categoria = paginator.page(page)
	except PageNotAnInteger:
		categoria = paginator.page(1)
	except EmptyPage:
		categoria = paginator.page(paginator.num_pages)

	context = {'error':error,'exito':exito,'categorias':categoria}
	return render(request, 'VendedorTemplates/registrarCategoria.html', context)



@permission_required('SIGPAd.view_seller')
def ingresarProducto(request):
	error = ''
	exito = ''
	categorias = Categoria.objects.all()
	consulta = request.GET.get('consulta')

	if consulta:
		categorias = categorias.filter(
			Q(nombre__icontains = consulta)|
			Q(codigo__icontains = consulta)
			).distinct()
	paginator = Paginator(categorias, 7)
	parametros = request.GET.copy()
	if parametros.has_key('page'):
		del parametros['page']
	
	page = request.GET.get('page')
	try:
		categoria = paginator.page(page)
	except PageNotAnInteger:
		categoria = paginator.page(1)
	except EmptyPage:
		categoria = paginator.page(paginator.num_pages)

	context = {'error':error,'exito':exito,'categorias':categoria,'parametros':parametros}
	return render(request, 'VendedorTemplates/ingresarProducto.html', context)



@permission_required('SIGPAd.view_seller')
def registrarProducto(request,pk):
	error = ''
	exito = ''
	cat = 'No selecciono una categoria'
	if request.method=='POST':
		codigo = request.POST.get('codigo',None)
		nombre = request.POST.get('nombre',None)
		descripcion = request.POST.get('descripcion',None)
		marca = request.POST.get('marca',None)
		if codigo!=None and nombre!=None and descripcion!=None and marca!=None:
			try:
				inventario = Inventario()
				inventario.save()
				producto = Producto()
				producto.categoria_id = pk
				producto.inventario_id=inventario.id
				producto.codigo=codigo
				producto.nombre=nombre
				producto.marca=marca
				producto.descripcion=descripcion
				producto.save()
				exito='Producto guardado con exito'
			except Exception as e:
				print(e.message)
				if 'column codigo is not unique' in e.message:
					error = 'Codigo de producto no es unico'
				if 'column nombre is not unique' in e.message:
					error='El nombre del producto debe ser unico'

	try:
		categoria = Categoria.objects.get(pk=pk)
		cat = categoria.nombre
	except Exception as e:
		error = 'Esa categoria no existe'


	productos = categoria.producto_set.all()
	
	consulta = request.GET.get('consulta')
	if consulta:
		categorias = productos.filter(
			Q(nombre__icontains = consulta)|
			Q(codigo__icontains = consulta)
			).distinct()
		productos=categorias
	paginator = Paginator(productos, 7)
	parametros = request.GET.copy()
	if parametros.has_key('page'):
		del parametros['page']
	
	page = request.GET.get('page')
	try:
		producto = paginator.page(page)
	except PageNotAnInteger:
		producto = paginator.page(1)
	except EmptyPage:
		producto = paginator.page(paginator.num_pages)

	context = {'error':error,'exito':exito,'categoria':cat,'productos':producto,'categorias':categoria,}
	return render(request, 'VendedorTemplates/registrarProducto.html', context)



@permission_required('SIGPAd.view_seller')
def mostrarProducto(request,pk):
	error = ''
	exito = ''
	productos = Producto.objects.filter(categoria_id=pk)
	consulta = request.GET.get('consulta')
	if consulta:
		categorias = productos.filter(
			Q(nombre__icontains = consulta)|
			Q(codigo__icontains = consulta)
			).distinct()
		productos=categorias
	paginator = Paginator(productos, 7)
	parametros = request.GET.copy()
	if parametros.has_key('page'):
		del parametros['page']
	
	page = request.GET.get('page')
	try:
		producto = paginator.page(page)
	except PageNotAnInteger:
		producto = paginator.page(1)
	except EmptyPage:
		producto = paginator.page(paginator.num_pages)

	context = {
		'error':error,
		'exito':exito,
		'productos':producto,
		'parametros':parametros,
	}
	return render(request, 'VendedorTemplates/mostrarProducto.html', context)

@permission_required('SIGPAd.view_seller')
def editarProducto(request, pk):
	exito = None
	existe = None
	error = None
	try:
		producto = Producto.objects.get(pk=pk)
	except Producto.DoesNotExist:
		producto = None

	if producto is not None:
		if request.method == 'POST':
			try:
				producto.nombre = request.POST.get('nombre',None)
				producto.marca = request.POST.get('marca',None)
				producto.descripcion = request.POST.get('descripcion',None)
				producto.save()
				exito='Producto guardado con exito'
			except Exception as e:
				print(e.message)
				if 'column codigo is not unique' in e.message:
					error = 'Codigo de producto no es unico'
				if 'column nombre is not unique' in e.message:
					error='El nombre del producto debe ser unico'
		else:
			context = {
				'producto':producto,
				'exito':exito,
				'error':error
			}
		
		context = {
				'producto':producto,
				'exito':exito,
				'error':error

			}
		return render(request,"VendedorTemplates/editarProducto.html", context) 

	else:
		existe = "El producto no existe"
		context = {
			'producto':producto,
			'existe':existe,
			'mensaje':mensaje,
		}
		return render(request,"VendedorTemplates/editarProducto.html", context)

@permission_required('SIGPAd.view_seller')
def productoEliminado(request,pk):
	error = ''
	exito = ''
	productos = Producto.objects.filter(estado=0)
	consulta = request.GET.get('consulta')
	if consulta:
		categorias = productos.filter(
			Q(nombre__icontains = consulta)|
			Q(codigo__icontains = consulta)
			).distinct()
		productos=categorias
	paginator = Paginator(productos, 7)
	parametros = request.GET.copy()
	if parametros.has_key('page'):
		del parametros['page']
	
	page = request.GET.get('page')
	try:
		producto = paginator.page(page)
	except PageNotAnInteger:
		producto = paginator.page(1)
	except EmptyPage:
		producto = paginator.page(paginator.num_pages)

	context = {
		'error':error,
		'exito':exito,
		'productos':producto,
		'parametros':parametros,
	}
	return render(request, 'VendedorTemplates/productoEliminado.html', context)

@permission_required('SIGPAd.view_seller')
def eliminarProducto(request, pk):
	error=None
	exito=None
	try:
		producto=Producto.objects.get(pk=pk)
	except Producto.DoesNotExist:
		producto = None
	if producto is not None:
		producto.estado=0
		producto.save()
		exito='Producto eliminado'
		context={'exito':exito,
		    'error':error,
		    }
	else:
		error='Producto no eliminado'
		context={'error':error,
		    'exito':exito,
		    }
	productos = Producto.objects.filter(estado=1)
	consulta = request.GET.get('consulta')
	if consulta:
		categorias = productos.filter(
			Q(nombre__icontains = consulta)|
			Q(codigo__icontains = consulta)
			).distinct()
		productos=categorias
	paginator = Paginator(productos, 7)
	parametros = request.GET.copy()
	if parametros.has_key('page'):
		del parametros['page']
	
	page = request.GET.get('page')
	try:
		producto = paginator.page(page)
	except PageNotAnInteger:
		producto = paginator.page(1)
	except EmptyPage:
		producto = paginator.page(paginator.num_pages)

	context = {
		'error':error,
		'exito':exito,
		'productos':producto,
		'parametros':parametros,
	}
	return render(request,'VendedorTemplates/mostrarProducto.html',context)

@permission_required('SIGPAd.view_seller')
def activarProducto(request, pk):
	error=None
	exito=None
	try:
		producto=Producto.objects.get(pk=pk)
	except Producto.DoesNotExist:
		producto = None
	if producto is not None:
		producto.estado=1
		producto.save()
		exito='Producto activado'
		context={'exito':exito,
		    'error':error,
		    }
	else:
		error='Producto no activado'
		context={'error':error,
		    'exito':exito,
		    }
	productos = Producto.objects.filter(estado=0)
	consulta = request.GET.get('consulta')
	if consulta:
		categorias = productos.filter(
			Q(nombre__icontains = consulta)|
			Q(codigo__icontains = consulta)
			).distinct()
		productos=categorias
	paginator = Paginator(productos, 7)
	parametros = request.GET.copy()
	if parametros.has_key('page'):
		del parametros['page']
	
	page = request.GET.get('page')
	try:
		producto = paginator.page(page)
	except PageNotAnInteger:
		producto = paginator.page(1)
	except EmptyPage:
		producto = paginator.page(paginator.num_pages)

	context = {
		'error':error,
		'exito':exito,
		'productos':producto,
		'parametros':parametros,
	}
	return render(request,'VendedorTemplates/productoEliminado.html',context)

@permission_required('SIGPAd.view_seller')
def registrarVenta(request):
	if request.method == 'POST':
		productos_cantidad = int(request.POST.get('productosCantidad'))
		elementos = int(request.POST.get('cantidad'))
		if(productos_cantidad <= 0):						
			return render(request, 'VendedorTemplates/ingresarVenta.html',{'alerta':'Seleccione un producto para realizar una venta'})
		venta = Venta()
		venta.empleado = Empleado.objects.get(usuario=request.user)
		venta.iva_venta = 0	
		venta.descripcion = request.POST.get('descripcionVenta')
		venta.total_venta =  0
		venta.save()		
		for x in range(1,elementos+1):
			codigo = request.POST.get('codigo-{}'.format(x),None)
			productos_anadidos_kardex = False
			if codigo!=None:
				cantidad = request.POST.get('cantidad-{}'.format(x),None)
				p = Producto.objects.get(codigo=codigo)
				p.inventario.existencia = p.inventario.existencia - int(cantidad)				
				detalle_venta = DetalleVenta()				
				detalle_venta.producto = p
				detalle_venta.venta = venta
				detalle_venta.cantidad = int(cantidad)
				detalle_venta.precio_unitario = p.inventario.precio_venta_producto
				detalle_venta.descuento = Decimal(request.POST.get('descuento-{}'.format(x),None))*100
				detalle_venta.total = round (Decimal(Decimal(detalle_venta.cantidad*detalle_venta.precio_unitario) -(Decimal(detalle_venta.cantidad*detalle_venta.precio_unitario)*Decimal(detalle_venta.descuento/100))),2)			
				venta.total_venta =  round(Decimal(venta.total_venta) + Decimal(detalle_venta.total),2)
				detalle_venta.save()
				id_prod = p.id
				productos_anadidos_kardex = nuevoKardex(2,id_prod,detalle_venta.cantidad,0)
				p.inventario.save()	
		cliente_usuario = request.POST.get('select-js',None)
		if(cliente_usuario):
			cliente = Cliente.objects.get(usuario__username=cliente_usuario)
			venta.cliente = cliente
			venta.nombre_cliente = cliente.nombre
			venta.dui_cliente = cliente.dui
			venta.save()
		venta.save()
		detalles = DetalleVenta.objects.filter(venta=venta)
		detalle_ingreso = productos_anadidos_kardex
		return redirect('/facturaVenta/{}'.format(venta.id))	
	return render(request, 'VendedorTemplates/ingresarVenta.html',{})

@permission_required('SIGPAd.view_seller')
def mostrarVenta(request):
	ventas = Venta.objects.all()
	return render(request, 'VendedorTemplates/mostrarVenta.html',{'ventas':ventas})

@permission_required('SIGPAd.view_seller')
def facturaVenta(request,id):
	venta = Venta.objects.get(id=id)
	factura = DetalleVenta.objects.filter(venta=venta)
	return render(request,'VendedorTemplates/facturaVenta.html',{'vendido':factura, 'empleado':venta.empleado, 'cliente':venta.cliente, 'total':venta.total_venta,'venta_id':venta.id})

@permission_required('SIGPAd.view_seller')
def productoDisponible(request):
	producto = serializers.serialize("json", Producto.objects.filter(inventario__existencia__gte=1).exclude(inventario__precio_venta_producto=0),use_natural_foreign_keys=True)
	return HttpResponse(producto, content_type='application/json')


@permission_required('SIGPAd.view_seller')
def clienteRegistrado(request):
	cliente = serializers.serialize("json", Cliente.objects.all(),use_natural_foreign_keys=True,fields=('usuario'))
	return HttpResponse(cliente, content_type='application/json')

#Vista de Compra.
@permission_required('SIGPAd.view_seller')
def listado_de_compras(request):
	compras = Compra.objects.all()
	"""paginator = Paginator(compras_listado, 2)
	page = request.GET.get('page')

	try:
		compras = paginator.page(page)
	except PageNotAnInteger:
		compras = paginator.page(1)
	except EmptyPage:
		compras = paginator.page(paginator.num_pages)"""

	context = {
		'compras':compras,
	}
	return render(request, 'VendedorTemplates/listadoCompras.html', context)


@permission_required('SIGPAd.view_seller')
def nueva_compra(request):
	usuario = request.user
	empleado = Empleado.objects.get(usuario=usuario)
	proveedores = Proveedor.objects.filter(estado=True)
	productos = Producto.objects.filter(estado=1)
	fecha_hora = datetime.now().strftime('%d/%m/%Y %H:%M:%S')

	try:
		if request.method == 'POST':
			compra = Compra()
			compra.empleado = empleado
			if proveedores:
				prov = Proveedor.objects.get(id=request.POST.get('idproveedor', None))
				compra.proveedor = prov
			compra.total_compra = request.POST.get('total_input',None)
			compra.total_compra_iva = request.POST.get('total_iva_input',None)
			compra.descripcion = request.POST.get('descripcion',None)
			compra.fecha_hora = datetime.now()
			compra.save()

			#idproducto = request.POST.get('idproducto',None)
			idproducto = request.POST.getlist('idproducto[]')
			cantidad = request.POST.getlist('cantidad[]')
			precio_compra = request.POST.getlist('precio_compra[]')
			descuento = request.POST.getlist('descuento[]')

			contador = 0

			while(contador < len(idproducto)):
				detalle_compra = DetalleCompra()
				detalle_compra.compra = compra
				detalle_compra.producto_id = idproducto[contador]
				inventario = Inventario.objects.get(producto__id=idproducto[contador])
				detalle_compra.cantidad = cantidad[contador]
				detalle_compra.precio_compra = precio_compra[contador]
				detalle_compra.descuento = descuento[contador]
				inventario.existencia = int(inventario.existencia) + int(cantidad[contador])
				inventario.save()
				detalle_compra.save()
				contador = contador + 1

			context = {
				'exito':"Exito",
				'proveedores':proveedores,
				'productos': productos,
				'usuario':usuario,
				'empleado':empleado,
				'fecha_hora':fecha_hora,
			}
			return redirect('/facturarCompra/{}'.format(compra.id))
		else:
			context = {
				'proveedores':proveedores,
				'productos':productos,
				'usuario':usuario,
				'empleado':empleado,
				'fecha_hora':fecha_hora,
			}
			return render(request, 'VendedorTemplates/nuevaCompra.html', context)
	except Exception as e:
		context = {
				'error':"Ha ocurrido un error, vuelva a intentarlo.",
				'proveedores':proveedores,
				'productos': productos,
				'usuario':usuario,
				'empleado':empleado,
				'fecha_hora':fecha_hora,
			}
	return render(request, 'VendedorTemplates/nuevaCompra.html', context)

@permission_required('SIGPAd.view_seller')
def cancelar_compra(request):
	return render(request,'VendedorTemplates/cancelarCompra.html',{})

@permission_required('SIGPAd.view_seller')
def facturar_compra(request, id):
	compra = get_object_or_404(Compra, id=id)
	detalle_compra = DetalleCompra.objects.filter(compra_id=id)
	context = {
		'compra': compra,
		'detalle_compra': detalle_compra,
	}
	return render(request,'VendedorTemplates/facturarCompra.html',context)

def reporte_compra(request, id):
	compra = get_object_or_404(Compra, id=id)
	detalle_compra = DetalleCompra.objects.filter(compra_id=id)
	return generar_reporte_compra(request, compra, detalle_compra)
#Fin vistas de Compras.	

@permission_required('SIGPAd.view_seller')
def subirExcel(request):
	exito=''
	error=''
	if request.method=='POST':
		action = request.POST.get('action')
		if action=='excelProducto':
			exito = 'Operacion realizada con exito'
			archivo = request.FILES.get('arch',None)
			doc=openpyxl.load_workbook(archivo)
			try:
				hoja1 = doc.get_sheet_by_name('Hoja1')
				for filas in hoja1.rows:
					try:
						producto = Producto() 
						i = 0
						for columna in filas:
							i +=1
							if i==1:
								cat = Categoria.objects.get(codigo=columna.value)
								producto.categoria=cat
							elif i==2:
								producto.codigo=columna.value
							elif i==3:
								producto.nombre=columna.value
							elif i==4:
								producto.marca=columna.value
							elif i==5:
								producto.descripcion=columna.value
						inventario = Inventario()
						inventario.save()
						producto.inventario=inventario
						producto.save()
						print(producto)
					except Exception as e:
						print('Error:'+e.message)
						error = 'Error desconocido, contacte al administrador'
						if 'Categoria matching query does not exist.' in e.message:
							error = 'Algunos productos no poseen categoria asignada'
						if 'column codigo is not unique' in e.message:
							error = 'Algunos productos tenian claves unicas'
						if 'column nombre is not unique' in e.message:
							error='Los nombres no eran unicos, ya estan esa lista de productos'
						exito=''
			except Exception as e:
				print(e.message)
				if 'column codigo is not unique' in e.message:
					error = 'El codigo no es unico, revise el excel y elimine las claves unicas '
					exito=''
				elif 'Worksheet Hoja does not exist.' in e.message:
					error = 'El nombre de la hoja tiene que ser: \"Hoja1\"'
					exito=''
		elif action=='excelCategoria':
			exito = 'Operacion realizada con exito'
			archivo = request.FILES.get('arch',None)
			doc=openpyxl.load_workbook(archivo)
			try:
				hoja1 = doc.get_sheet_by_name('Hoja1')
				for filas in hoja1.rows:
					try: 
						categoria = Categoria()
						i = 0
						for columna in filas:
							i +=1
							if i==1:
								categoria.codigo=columna.value
							elif i==2:
								categoria.nombre=columna.value
							elif i ==3:
								categoria.descripcion=columna.value
						categoria.save()
						print(categoria)
					except Exception as e:
						print (e)
						error = 'Algunas categorias tenian claves unicas'
						exito=''
						categoria.delete()
			except Exception as e:
				print(e.message)
				if 'column codigo is not unique' in e.message:
					error = 'El codigo no es unico, revise el excel y elimine las claves unicas '
					exito=''
				elif 'Worksheet Hoja does not exist.' in e.message:
					error = 'El nombre de la hoja tiene que ser: \"Hoja1\"'
					exito=''

	context = {'exito':exito,'error':error}
	return render(request, 'VendedorTemplates/subirExcel.html', context)

@permission_required('SIGPAd.view_seller')
def mostrarInventario(request):
	consulta = request.GET.get('consulta')
	producto = Producto.objects.all()
	if consulta:
		producto = producto.filter(
			Q(nombre__icontains = consulta)|
			Q(codigo__icontains = consulta)
			).distinct()
	paginator = Paginator(producto, 7)
	parametros = request.GET.copy()
	if parametros.has_key('page'):
		del parametros['page']
	
	page = request.GET.get('page')
	try:
		producto = paginator.page(page)
	except PageNotAnInteger:
		producto = paginator.page(1)
	except EmptyPage:
		producto = paginator.page(paginator.num_pages)

	context={'producto':producto}
	return render(request,'VendedorTemplates/inventario.html',context)


def enviarCorreo():
	try:
		msg = MIMEMultipart()
		password = "toor215IDS"
		msg['From'] = "compuofertaSDI215@gmail.com"
		msg['To'] = "christianfuentes254@gmail.com"
		msg['Subject'] = "Inventario critico"
		message = "Saludos: {} , le informamos que algun producto tiene bajas existencias en el inventario, por favor abastecer dicho producto.... le saludamos y esparamos resuelva esto ALV".format(msg['To'])
		msg.attach(MIMEText(message, 'plain'))
		server = smtplib.SMTP('smtp.gmail.com: 587')
		server.starttls()
		server.login(msg['From'], password)
		server.sendmail(msg['From'], msg['To'], msg.as_string())
		server.quit()
		print("successfully sent email to %s:" % (msg['To']))
		return "successfully sent email to %s:" % (msg['To'])
	except Exception as e:
		return "Error, mensaje fallido al administrador, para anunciar el inventario {}".format(e.message)

def mostrarKardex(request, pk):
	try:
		consulta = request.GET.get('consulta')
		producto = Producto.objects.get(pk=pk)
		kardex_producto = Kardex.objects.filter(producto=producto)
		ultimo = kardex_producto.last()
		if ultimo:
			precio_sugerido = round((Decimal(ultimo.precExistencia) * Decimal(1.25)),2)
		else:
			precio_sugerido = 0
		fech = datetime.now()
		anio = fech.year
		if consulta:
			kardex_producto = kardex_producto.filter(
				Q(fecha__icontains = consulta)).distinct()
		else:
			kardex_producto = kardex_producto.filter(
				Q(fecha__icontains = anio)).distinct()
		paginator = Paginator(kardex_producto, 7)
		parametros = request.GET.copy()
		if parametros.has_key('page'):
			del parametros['page']
		
		page = request.GET.get('page')
		try:
			kardex_producto = paginator.page(page)
		except PageNotAnInteger:
			kardex_producto = paginator.page(1)
		except EmptyPage:
			producto = paginator.page(paginator.num_pages)

		if request.method=='POST':
			precio = request.POST.get('nuevoPrecio',None)
			if precio != None:
				pr = int(precio)
				if pr >= 0:
					inventario = producto.inventario
					inventario.precio_venta_producto = precio
					inventario.save()
		context = {
			'producto':producto,
			'kardex':kardex_producto,
			'fecha':fech,
			'ultimo':ultimo,
			'precio_sugerido':precio_sugerido,
		}
		return render(request,'VendedorTemplates/kardex.html',context)
	except Producto.DoesNotExist:
		context={'error':'producto no existe'}
		return render(request,'VendedorTemplates/kardex.html',context)

@permission_required('SIGPAd.view_seller')

def grafica(request):
	return render_to_response('VendedorTemplates/grafica.html',context)

def graficaMes(request):
	venta=Venta.objects.all()
	fechas=[obj.fecha_hora for obj in venta]
	anioActual=datetime.now()
	anio=int(str(anioActual.strftime('%Y')))
	anio1=anio-1
	anio2=anio-2
	anioAnterior = ''
	mes1=0
	mes2=0
	mes3=0
	mes4=0
	mes5=0
	mes6=0
	mes7=0
	mes8=0
	mes9=0
	mes10=0
	mes11=0
	mes12=0

	if request.method=='POST':
		anioAnterior = request.POST.get('anioAnterior',None)

	if anioAnterior=='anio':
		anioAnterior=2018
	if anioAnterior=='anio1':
		anio=anio-1
		anioAnterior=2017
	if anioAnterior=='anio2':
		anio=anio-2
		anioAnterior=2016

	enero=datetime(anio, 1, 1)
	febrero=datetime(anio, 2, 1)
	marzo=datetime(anio, 3, 1)
	abril=datetime(anio, 4, 1)
	mayo=datetime(anio, 5, 1)
	junio=datetime(anio, 6, 1)
	julio=datetime(anio, 7, 1)
	agosto=datetime(anio, 8, 1)
	septiembre=datetime(anio, 9, 1)
	octubre=datetime(anio, 10, 1)
	noviembre=datetime(anio, 11, 1)
	diciembre=datetime(anio, 12, 1)

	for fecha in fechas:
		if str(fecha) >= str(enero.strftime('%Y-%m-%d')) and str(fecha) < str(febrero.strftime('%Y-%m-%d')):
			mes1=mes1+1
		if str(fecha) >= str(febrero.strftime('%Y-%m-%d')) and str(fecha) < str(marzo.strftime('%Y-%m-%d')):
			mes2=mes2+1
		if str(fecha) >= str(marzo.strftime('%Y-%m-%d')) and str(fecha) < str(abril.strftime('%Y-%m-%d')):
			mes3=mes3+1
		if str(fecha) >= str(abril.strftime('%Y-%m-%d')) and str(fecha) < str(mayo.strftime('%Y-%m-%d')):
			mes4=mes4+1
		if str(fecha) >= str(mayo.strftime('%Y-%m-%d')) and str(fecha) < str(junio.strftime('%Y-%m-%d')):
			mes5=mes5+1
		if str(fecha) >= str(junio.strftime('%Y-%m-%d')) and str(fecha) < str(julio.strftime('%Y-%m-%d')):
			mes6=mes6+1
		if str(fecha) >= str(julio.strftime('%Y-%m-%d')) and str(fecha) < str(agosto.strftime('%Y-%m-%d')):
			mes7=mes7+1
		if str(fecha) >= str(agosto.strftime('%Y-%m-%d')) and str(fecha) < str(septiembre.strftime('%Y-%m-%d')):
			mes8=mes8+1
		if str(fecha) >= str(septiembre.strftime('%Y-%m-%d')) and str(fecha) < str(octubre.strftime('%Y-%m-%d')):
			mes9=mes9+1
		if str(fecha) >= str(octubre.strftime('%Y-%m-%d')) and str(fecha) < str(noviembre.strftime('%Y-%m-%d')):
			mes10=mes10+1
		if str(fecha) >= str(noviembre.strftime('%Y-%m-%d')) and str(fecha) < str(diciembre.strftime('%Y-%m-%d')):
			mes11=mes11+1
		if str(fecha) >= str(diciembre.strftime('%Y-%m-%d')) and str(fecha) < str(enero.strftime('%Y-%m-%d')):
			mes12=mes12+1
	
	anio=int(str(anioActual.strftime('%Y')))
	meses=['enero','febrero','marzo','abril','mayo','junio','julio','agosto','septiembre','octubre','noviembre','diciembre']
	ventas=[mes1, mes2, mes3, mes4, mes5, mes6, mes7, mes8, mes9, mes10, mes11, mes12]
	context = {
        'meses': json.dumps(meses),
        'ventas': json.dumps(ventas),
        'anio':anio,
        'anio1':anio1,
        'anio2':anio2,
        'anioAnterior':anioAnterior,
    }

	return render(request, 'VendedorTemplates/graficaMes.html', context)

def graficaEmpleado(request):
	venta=''
	nom=''
	nomEmpleado = ''
	empleado=Empleado.objects.all()
	anioActual=datetime.now()
	anio=int(str(anioActual.strftime('%Y')))

	mes1=0
	mes2=0
	mes3=0
	mes4=0
	mes5=0
	mes6=0
	mes7=0
	mes8=0
	mes9=0
	mes10=0
	mes11=0
	mes12=0

	if request.method=='POST':
		nomEmpleado = request.POST.get('nomEmpleado',None)

	enero=datetime(anio, 1, 1)
	febrero=datetime(anio, 2, 1)
	marzo=datetime(anio, 3, 1)
	abril=datetime(anio, 4, 1)
	mayo=datetime(anio, 5, 1)
	junio=datetime(anio, 6, 1)
	julio=datetime(anio, 7, 1)
	agosto=datetime(anio, 8, 1)
	septiembre=datetime(anio, 9, 1)
	octubre=datetime(anio, 10, 1)
	noviembre=datetime(anio, 11, 1)
	diciembre=datetime(anio, 12, 1)

	if nomEmpleado:
		nom = Empleado.objects.filter(pk=nomEmpleado)
		venta = Venta.objects.filter(empleado=nomEmpleado)
		fechas=[obj.fecha_hora for obj in venta]
		for fecha in fechas:
			if str(fecha) >= str(enero.strftime('%Y-%m-%d')) and str(fecha) < str(febrero.strftime('%Y-%m-%d')):
				mes1=mes1+1
			if str(fecha) >= str(febrero.strftime('%Y-%m-%d')) and str(fecha) < str(marzo.strftime('%Y-%m-%d')):
				mes2=mes2+1
			if str(fecha) >= str(marzo.strftime('%Y-%m-%d')) and str(fecha) < str(abril.strftime('%Y-%m-%d')):
				mes3=mes3+1
			if str(fecha) >= str(abril.strftime('%Y-%m-%d')) and str(fecha) < str(mayo.strftime('%Y-%m-%d')):
				mes4=mes4+1
			if str(fecha) >= str(mayo.strftime('%Y-%m-%d')) and str(fecha) < str(junio.strftime('%Y-%m-%d')):
				mes5=mes5+1
			if str(fecha) >= str(junio.strftime('%Y-%m-%d')) and str(fecha) < str(julio.strftime('%Y-%m-%d')):
				mes6=mes6+1
			if str(fecha) >= str(julio.strftime('%Y-%m-%d')) and str(fecha) < str(agosto.strftime('%Y-%m-%d')):
				mes7=mes7+1
			if str(fecha) >= str(agosto.strftime('%Y-%m-%d')) and str(fecha) < str(septiembre.strftime('%Y-%m-%d')):
				mes8=mes8+1
			if str(fecha) >= str(septiembre.strftime('%Y-%m-%d')) and str(fecha) < str(octubre.strftime('%Y-%m-%d')):
				mes9=mes9+1
			if str(fecha) >= str(octubre.strftime('%Y-%m-%d')) and str(fecha) < str(noviembre.strftime('%Y-%m-%d')):
				mes10=mes10+1
			if str(fecha) >= str(noviembre.strftime('%Y-%m-%d')) and str(fecha) < str(diciembre.strftime('%Y-%m-%d')):
				mes11=mes11+1
			if str(fecha) >= str(diciembre.strftime('%Y-%m-%d')) and str(fecha) < str(enero.strftime('%Y-%m-%d')):
				mes12=mes12+1

	anio=int(str(anioActual.strftime('%Y')))
	meses=['enero','febrero','marzo','abril','mayo','junio','julio','agosto','septiembre','octubre','noviembre','diciembre']
	ventas=[mes1, mes2, mes3, mes4, mes5, mes6, mes7, mes8, mes9, mes10, mes11, mes12]
	context = {
        'meses': json.dumps(meses),
        'ventas': json.dumps(ventas),
        'anio':anio,
        'empleado':empleado,
        'venta':venta,
        'nom':nom,
        'nomEmpleado':nomEmpleado,
    }

	return render(request, 'VendedorTemplates/graficaEmpleado.html', context)

def graficaProducto(request):
	venta=''
	mes = ''
	mes1=0
	cantidades=''
	 
	producto=Producto.objects.all()
	productos=[obj.nombre for obj in producto]
	cant=len(productos)
	total = [0 for i in range(cant)]

	anioActual=datetime.now()
	anio=int(str(anioActual.strftime('%Y')))

	if request.method=='POST':
		mes = request.POST.get('mes',None)
	if mes=='enero':
		mes1=1
	if mes=='febrero':
		mes1=2
	if mes=='marzo':
		mes1=3
	if mes=='abril':
		mes1=4
	if mes=='mayo':
		mes1=5
	if mes=='junio':
		mes1=6
	if mes=='julio':
		mes1=7
	if mes=='agosto':
		mes1=8
	if mes=='septiembre':
		mes1=9
	if mes=='octubre':
		mes1=10
	if mes=='noviembre':
		mes1=11
	if mes=='diciembre':
		mes1=12

	j=0
	if mes:
		for p in productos:
			mes2=datetime(anio,mes1,1)
			mes_venta = mes2.strftime("%Y-%m")
			venta = Venta.objects.filter(Q(fecha_hora__icontains = mes_venta))
		
			cant1=len(venta)
			cantidades1 = [0 for i in range(cant1)]
			k=0

			for v in venta:
				nom = Producto.objects.filter(nombre=p)
				detalle_venta = DetalleVenta.objects.filter(producto=nom).filter(venta=v)
				cantidades=[obj.cantidad for obj in detalle_venta]
				cantidades1[k]=max(cantidades or [0])
				k=k+1
			print nom
			print cantidades1

			suma=0
			for i in cantidades1:
				suma=suma+i
			total[j]=suma
			j=j+1

	meses=['enero','febrero','marzo','abril','mayo','junio','julio','agosto','septiembre','octubre','noviembre','diciembre']
	context = {
        'meses': meses,
        'productos': json.dumps(productos),
        'total': json.dumps(total),

    }

	return render(request, 'VendedorTemplates/graficaProducto.html', context)