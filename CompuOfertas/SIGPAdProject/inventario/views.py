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


# Create your views here.
##No somos muy ordenados asique aqui vamos a empezar con el codigo del Sprint 2

#Vistas vendedores.
@permission_required('SIGPAd.view_seller')
def  indexVendedor(request):
	user = request.user
	error=''
	if request.method=='POST':
		error=enviarCorreo()
		print(error)
	
	if user.is_authenticated():
		if user.is_superuser:
			return render(request,'AdministradorTemplates/adminIndex.html',{})
		else:
			return render(request,'VendedorTemplates/vendedorIndex.html',{'error':error})			
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
						error='Lo el nombre se repite, intente nuevamente'
					if 'column codigo is not unique' in e.message:
						error='El codigo que esta insertando ya esta ocupado'
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
def registrarVenta(request):
	if request.method == 'POST':
		elementos = int(request.POST.get('cantidad'))
		venta = Venta()
		venta.empleado = Empleado.objects.get(usuario=request.user)
		venta.iva_venta = 0	
		venta.descripcion = 'No se que va aqui xd'
		venta.total_venta =  0
		venta.save()		
		for x in range(1,elementos+1):
			codigo = request.POST.get('codigo-{}'.format(x),None)				
			if codigo!=None:
				cantidad = request.POST.get('cantidad-{}'.format(x),None)
				p = Producto.objects.get(codigo=codigo)
				p.inventario.existencia = p.inventario.existencia - int(cantidad)				
				detalle_venta = DetalleVenta()				
				detalle_venta.producto = p
				detalle_venta.venta = venta
				detalle_venta.cantidad = int(cantidad)
				detalle_venta.precio_unitario = p.inventario.precio_venta_producto
				detalle_venta.descuento = 0				
				venta.total_venta =  round(Decimal(venta.total_venta) + Decimal(detalle_venta.cantidad*detalle_venta.precio_unitario),2)
				detalle_venta.save()
				p.inventario.save()	
		venta.save()
		return render(request,'VendedorTemplates/ingresarVenta.html',{})	
	return render(request, 'VendedorTemplates/ingresarVenta.html',{})

@permission_required('SIGPAd.view_seller')
def productoDisponible(request):
	producto = serializers.serialize("json", Producto.objects.filter(inventario__existencia__gte=1),use_natural_foreign_keys=True)
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
			context = {
				'proveedores':proveedores,
				'productos': productos,
				'usuario':usuario,
				'empleado':empleado,
				'fecha_hora':fecha_hora,
			}
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
		context = {'error':"Mensaje de error"}		
	return render(request, 'VendedorTemplates/nuevaCompra.html', context)
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

	context={'inventario':inventario,'producto':producto}
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




