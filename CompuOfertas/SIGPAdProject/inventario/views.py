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
			empleado = user.empleado_set.all().latest('nombre')
			return render(request,'VendedorTemplates/vendedorIndex.html',{'empleado':empleado})			
	return render_to_response('VendedorTemplates/vendedorIndex.html')


@permission_required('SIGPAd.view_seller')
def registrarCategoria(request):
	error = ''
	exito = ''
	empleado = request.user.empleado_set.all().latest('nombre')
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

	context = {'error':error,'exito':exito,'categorias':categoria,'empleado':empleado}
	return render(request, 'VendedorTemplates/registrarCategoria.html', context)



@permission_required('SIGPAd.view_seller')
def ingresarProducto(request):
	error = ''
	exito = ''
	categorias = Categoria.objects.all()
	consulta = request.GET.get('consulta')
	empleado = request.user.empleado_set.all().latest('nombre')

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

	context = {'error':error,'exito':exito,'categorias':categoria,'parametros':parametros,'empleado':empleado}
	return render(request, 'VendedorTemplates/ingresarProducto.html', context)



@permission_required('SIGPAd.view_seller')
def registrarProducto(request,pk):
	error = ''
	exito = ''
	cat = 'No selecciono una categoria'
	empleado = Empleado.objects.filter(usuario=request.user).latest('nombre')
	if request.method=='POST':
		codigo = request.POST.get('codigo',None)
		nombre = request.POST.get('nombre',None)
		descripcion = request.POST.get('descripcion',None)
		marca = request.POST.get('marca',None)
		if codigo!=None and nombre!=None and descripcion!=None and marca!=None:
			try:
				inventario = Inventario()
				inventario.sucursal=empleado.sucursal
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

	inventario = empleado.sucursal.inventario_set.all()
	p = []
	for x in inventario:
		p.append(x)

	productos = categoria.producto_set.all().filter(inventario__in=p)
	
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

	context = {'error':error,'exito':exito,'categoria':cat,'productos':producto,'categorias':categoria,'empleado':empleado}
	return render(request, 'VendedorTemplates/registrarProducto.html', context)



@permission_required('SIGPAd.view_seller')
def mostrarProducto(request,pk):
	error = ''
	exito = ''
	productos = Producto.objects.filter(categoria_id=pk)
	consulta = request.GET.get('consulta')
	empleado = request.user.empleado_set.all().latest('nombre')
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
		'empleado':empleado
	}
	return render(request, 'VendedorTemplates/mostrarProducto.html', context)

@permission_required('SIGPAd.view_seller')
def registrarVenta(request):
	if request.method == 'POST':
		elementos = int(request.POST.get('cantidad'))		
		for x in range(1,elementos+1):
			codigo = request.POST.get('codigo-{}'.format(x),None)	
			if codigo!=None:
				cantidad = request.POST.get('cantidad-{}'.format(x),None)
				p = Producto.objects.get(codigo=codigo)
				p.inventario.existencia = p.inventario.existencia - int(cantidad)					
				p.inventario.save()		
		return render(request,'VendedorTemplates/ingresarVenta.html',{})	
	return render(request, 'VendedorTemplates/ingresarVenta.html',{})

@permission_required('SIGPAd.view_seller')
def productoDisponible(request):
	producto = serializers.serialize("json", Producto.objects.filter(inventario__existencia__gte=1),use_natural_foreign_keys=True)
	return HttpResponse(producto, content_type='application/json')

<<<<<<< HEAD
@permission_required('SIGPAd.view_seller')
def clienteRegistrado(request):
	cliente = serializers.serialize("json", Cliente.objects.all(),use_natural_foreign_keys=True,fields=('usuario'))
	return HttpResponse(cliente, content_type='application/json')
=======
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
>>>>>>> a63c1a481aac7c269ff7fb7069eb510068c2c5e2

@permission_required('SIGPAd.view_seller')
def subirExcel(request):
	exito=''
	error=''
	empleado = Empleado.objects.filter(usuario=request.user).latest('nombre')
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
						inventario.sucursal=empleado.sucursal
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

	context = {'empleado':empleado,'exito':exito,'error':error}
	return render(request, 'VendedorTemplates/subirExcel.html', context)

@permission_required('SIGPAd.view_seller')
def mostrarInventario(request):
	empleado = Empleado.objects.filter(usuario=request.user).latest('nombre')
	inventario = Inventario.objects.filter(sucursal=empleado.sucursal)
	p = []
	for x in inventario:
		p.append(x)
	print(p)
	consulta = request.GET.get('consulta')

	producto = Producto.objects.filter(inventario__in=p)
	print(producto)
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

	context={'empleado':empleado,'inventario':inventario,'producto':producto}
	return render(request,'VendedorTemplates/inventario.html',context)


@permission_required('SIGPAd.view_seller')
def agregarProductoSucursal(request):
	empleado = Empleado.objects.filter(usuario=request.user).latest('nombre')
	sucursal = Sucursal.objects.all().exclude(pk=empleado.sucursal.id)
	context={'empleado':empleado,'sucursal':sucursal}
	return render(request,'VendedorTemplates/agregarProductoSucursal.html',context)

@permission_required('SIGPAd.view_seller')
def agregarPS(request,pk):
	empleado = Empleado.objects.filter(usuario=request.user).latest('nombre')
	sucursal = Sucursal.objects.all().exclude(pk=empleado.sucursal.id)
	exito=''
	error=''
	try:
		producto = Producto.objects.get(pk=pk)
		sucursalActual = Sucursal.objects.get(pk=empleado.sucursal.id)
		print(sucursalActual)
		insertar = True
		for i in sucursalActual.inventario_set.all():
			for p in i.producto_set.all():
				if producto.codigo in p.codigo :
					insertar = False
					error = 'lo siento ese producto ya esta en tu inventario'
			print('no esta')

		if insertar == True:
			inventario = Inventario()
			inventario.sucursal=empleado.sucursal
			inventario.save()
			p = Producto()
			p.categoria=producto.categoria
			p.inventario = inventario
			p.codigo = producto.codigo + str(empleado.sucursal.id)
			p.nombre = producto.nombre
			p.marca = producto.marca
			p.descripcion = producto.descripcion
			p.save()
			print('esta')
			exito='Nuevo producto en su sucursal listo para usar'
	except Exception as e:
		print(e.message)
		error='Lo siento ese producto ya esta en su sucursal'
	context={'empleado':empleado,'sucursal':sucursal,'error':error,'exito':exito}
	return render(request,'VendedorTemplates/agregarProductoSucursal.html',context)





