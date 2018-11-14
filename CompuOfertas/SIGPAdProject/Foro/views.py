# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.models import User,Permission
from django.contrib.auth.hashers import check_password
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.views.defaults import page_not_found
from .models import *
from django.db.models import Q
from django.core import serializers
import json 
from django.core.serializers.json import DjangoJSONEncoder
from inventario.models import *
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist
from SIGPAd.models import *

# Create your views here.
def ForoIndex(request):
	return render(request, 'exterior/foro.html', {})

@login_required
def MiniChat(request):
	yo = request.user
	context = {
		'yo':yo,
	}
	return render(request, 'cliente/mini_chat.html', context)

#@permission_required('SIGPAd.es_cliente')
def mensajes(request,pk):
	user = request.user
	error = ''
	chats = Chat.objects.filter(receptor=user) 
	chats2 = Chat.objects.filter(emisor=user.username)
	datos = []
	for x in chats:
		us = User.objects.get(username=x.emisor)
		datos.append(us)

	for x in chats2:
		if x.receptor in datos:
			pass
		else:
			datos.append(x.receptor)

	contactos = datos
	print(contactos)
	chat = None
	primer = None
	try:
		primer = User.objects.get(pk=pk)
		chat =Chat.objects.all()
		chat=chat.filter(Q(receptor=primer,emisor=user.username)|Q(receptor=user,emisor=primer.username)).distinct().first()
		msj = chat.mensaje_set.all().filter(estado=0)
		for x in msj:
			x.estado=1
			x.save()
		if request.method == 'POST':
			c = request.POST.get('msg',None)
			chat.ultimo=c
			chat.save()
			mens = Mensaje(chat=chat,msj=c,enviado=user.id)
			mens.save()
	except Exception as e:
		print(e.message)
		if 'object has no attribute' in e.message:
			error=''
			if request.method == 'POST':
				c = request.POST.get('msg',None)
				print(c)
				chat = Chat(emisor=user.username,receptor=primer, conectado=1,estado=1,ultimo=c)
				chat.save()
				mens = Mensaje(chat=chat,msj=c,enviado=user.id)
				mens.save()
	consulta = request.GET.get('consulta')
	if consulta:
		cont = []
		for x in contactos:
			if consulta in x.username:
				cont.append(x)
		contactos = cont
		primer=None
		chat=None
	contexto={'contactos':contactos,'primer':primer,'chat':chat,'yo':user,'error':error}
	if user.empleado_set.all():
		return render(request,'VendedorTemplates/vendedorMensaje.html',contexto)
	else:
		return render(request,'cliente/mensajes.html',contexto)

def nuevoMensaje(request):
	user = request.user
	consulta = request.GET.get('consulta')
	empleados = Empleado.objects.filter(estado=1).exclude(usuario=user)
	cliente = Cliente.objects.filter(estado=1).exclude(usuario=user)
	if consulta:
		empleados = empleados.filter(
			Q(nombre__icontains = consulta)|
			Q(usuario__username__icontains = consulta)
			).distinct()
		cliente = cliente.filter(
			Q(nombre__icontains = consulta)|
			Q(usuario__username__icontains = consulta)
			).distinct()

	paginator = Paginator(empleados, 5)
	parametros = request.GET.copy()
	if parametros.has_key('pageEm'):
		del parametros['pageEm']
	page = request.GET.get('pageEm')
	try:
		empleados = paginator.page(page)
	except PageNotAnInteger:
		empleados = paginator.page(1)
	except EmptyPage:
		empleados = paginator.page(paginator.num_pages)

	paginator = Paginator(cliente, 5)
	parametros = request.GET.copy()
	if parametros.has_key('pageCl'):
		del parametros['pageCl']
	page = request.GET.get('pageCl')
	try:
		cliente = paginator.page(page)
	except PageNotAnInteger:
		cliente = paginator.page(1)
	except EmptyPage:
		cliente = paginator.page(paginator.num_pages)

	if request.method=='POST':
		id_user = request.POST.get('id_usuario',None) 
		new_contactos = User.objects.get(pk=id_user)
		try:
			c = request.POST.get('mensaje',None)
			chat = Chat.objects.get(receptor=new_contactos,emisor=user.username)
			chat.ultimo=c
			chat.estado=0
			chat.save()
			mens = Mensaje(chat=chat,msj=c,enviado=user.id)
			mens.save()
		except Chat.DoesNotExist:
			try:
				chat2 = Chat.objects.get(receptor=user,emisor=new_contactos.username)
				chat2.ultimo=c
				chat2.estado=0
				chat2.save()
				mens = Mensaje(chat=chat2,msj=c,enviado=user.id)
				mens.save()
			except Chat.DoesNotExist:
				c = request.POST.get('mensaje',None)
				print(c)
				chat = Chat(emisor=user.username,receptor=new_contactos, conectado=1,estado=1,ultimo=c)
				chat.save()
				mens = Mensaje(chat=chat,msj=c,enviado=user.id)
				mens.save()
		return redirect("/mensajes/0")

	contexto={'usuarios':empleados,'clientes':cliente,'yo':user}
	if user.empleado_set.all():
		return render(request,'VendedorTemplates/vendedorNuevoMsj.html',contexto)
	else:
		return render(request,'cliente/nuevoMensaje.html',contexto)


def enviarNuevoMensaje(request, pk):
	user = request.user
	new_contactos = User.objects.get(pk=pk)
	if request.method=='POST':
		try:
			c = request.POST.get('msg',None)
			chat = Chat.objects.get(receptor=new_contactos,emisor=user.username)
			chat.ultimo=c
			chat.estado=0
			chat.save()
			mens = Mensaje(chat=chat,msj=c,enviado=user.id)
			mens.save()
		except Chat.DoesNotExist:
			try:
				chat2 = Chat.objects.get(receptor=user,emisor=new_contactos.username)
				chat2.ultimo=c
				chat2.estado=0
				chat2.save()
				mens = Mensaje(chat=chat2,msj=c,enviado=user.id)
				mens.save()
			except Chat.DoesNotExist:
				c = request.POST.get('msg',None)
				print(c)
				chat = Chat(emisor=user.username,receptor=new_contactos, conectado=1,estado=1,ultimo=c)
				chat.save()
				mens = Mensaje(chat=chat,msj=c,enviado=user.id)
				mens.save()
		return redirect("/mensajes/0")

	contexto={'contactos':new_contactos,'yo':user}
	return render(request,'cliente/enviarNuevoMensaje.html',contexto)


def servicio_mensajeria(request,emisor_id,receptor_id): #chat
	user = request.user
	if user.id==int(emisor_id) or user.id==int(receptor_id):
		mensajes = json.dumps(list(getChat(emisor_id,receptor_id,True,user.id)), cls=DjangoJSONEncoder)
	else:
		mensajes = serializers.serialize("json",[],use_natural_foreign_keys=True)
	return HttpResponse(mensajes, content_type='application/json')


def getChat(id_emisor,id_receptor,contactos,id):
	chat = None
	primer = None
	user = None
	try:
		primer = User.objects.get(pk=id_receptor)
		user = User.objects.get(pk=id_emisor)
		if contactos:
			datos = []
			chat =Chat.objects.all()
			chat=chat.filter(Q(receptor=primer,emisor=user.username)|Q(receptor=user,emisor=primer.username)).distinct().first()
			c = chat.mensaje_set.all().filter(estado=0).exclude(enviado=id)
			for x in c:
				x.estado=1
				x.save()
				img = ''
				datos.append({"model":"Foro.mensaje","pk":x.id,"fields":{"ids":x.id,"msj":x.msj,"img":img}})
			return datos
	except Exception as e:
		return []


def servicio_chat(request): #notificacion
	user = request.user
	#ch = serializers.serialize("json",getChatUser(user),use_natural_foreign_keys=True)
	ch = json.dumps(list(getChatUser(user)), cls=DjangoJSONEncoder)
	return HttpResponse(ch, content_type='application/json')


def getChatUser(user):
	chats = Chat.objects.filter(receptor=user)
	chats2 = Chat.objects.filter(emisor=user.username)
	datos = []
	for x in chats:
		m1 = x.mensaje_set.all().filter(estado=0)
		val = len(m1)
		if val > 0:
			m = m1.latest("id")
			if m.enviado != user.id:
				mens = ''
				if len(m.msj)>40:
					mens = m.msj[:40:1]
				else:
					val = 40 - len(m.msj)
					mens = m.msj+" " + "_"*val 
				datos.append({"model":"Foro.mensaje","pk":m.id,"fields":{"ids":m.id,"msj":mens,"username":x.emisor,"enviado":m.enviado,"fecha":m.fecha_hora.strftime("%d-%m-%y %H:%M:%S")}})
	for x in chats2:
		m1 = x.mensaje_set.all().filter(estado=0)
		val = len(m1)
		if val > 0 :
			m = m1.latest("id")
			if m.enviado != user.id:
				mens = ''
				if len(m.msj)>40:
					mens = m.msj[:40:1]
				else:
					val = 40 - len(m.msj)
					mens = m.msj+" " + "_"*val 
				datos.append({"model":"Foro.mensaje","pk":m.id, "fields":{"ids":m.id,"msj":mens,"username":x.receptor.username,"enviado":m.enviado,"fecha":m.fecha_hora.strftime("%d-%m-%y %H:%M:%S")}})
	return datos


def get_servicio_mini_chat(request,receptor_id): #El emisor, no se necesita para estar logeado.
	user = request.user
	mensajes = serializers.serialize("json",get_parametros_mini_chat(user.id,receptor_id),use_natural_foreign_keys=True)
	return HttpResponse(mensajes, content_type='application/json')


def get_parametros_mini_chat(id_emisor,id_receptor):
	try:
		primer = User.objects.get(pk=id_emisor)
		user = User.objects.get(pk=id_receptor)
		chat =Chat.objects.all()
		chat=chat.filter(Q(receptor=primer,emisor=user.username)|Q(receptor=user,emisor=primer.username)).distinct().first()
		return chat.mensaje_set.all()
	except Exception as e:
		return []

def enviar_mensajes_mini_chat(id_emisor,id_receptor, mensaje):
	try:
		primer = User.objects.get(pk=id_emisor)
		user = User.objects.get(pk=id_receptor)
		chat =Chat.objects.all()
		chat=chat.filter(Q(receptor=primer,emisor=user.username)|Q(receptor=user,emisor=primer.username)).distinct().first()
		chat.ultimo = mensaje
		chat.save()
		msg =  Mensaje(chat=chat,msj=mensaje,enviado=primer.id)
		msg.save()
		return True

	except Exception as e:
		return False

def articulo(request):
	try:
		articulos = Producto.objects.filter(inventario__existencia__gte=1).exclude(Q(inventario__precio_venta_producto=0) ).exclude(img='')
		if articulos:
			contexto = paginacion_productos(request,articulos,6)
			return render(request, 'cliente/articulos.html', contexto)
		else:
			return render(request, 'cliente/articulos.html', {'error':'No hay productos para mostrar'})
	except Producto.DoesNotExist:
		return render(request, 'cliente/articulos.html', {'error':'Ocurrió un error'})
	

def detalleArticulo(request, id):
	try:
		detalle = Producto.objects.filter(inventario__existencia__gte=1).exclude(Q(inventario__precio_venta_producto=0) ).exclude(img='').get(id=id)
		mi_valoracion = Valoracion.objects.get(Q(producto = detalle) & Q(usuario=request.user))	
		contexto = {'art': detalle, 'puntuacion':mi_valoracion.puntuacion}
		if request.method == 'POST':		
			try:
				estrellas = request.POST.get('estrellas')			
				if (estrellas):
					mi_puntuacion = int(estrellas)
					if(mi_puntuacion<1 or mi_puntuacion>5):					
						messages.error(request, 'La puntuacion debe estar entre 1 y 5')						
						return redirect('/detalleArticulo/{}'.format(detalle.id))
					else:
						mi_valoracion.puntuacion = mi_puntuacion					
						mi_valoracion.save()
						total = Valoracion.objects.filter(Q(producto = detalle) & Q(puntuacion__gte = 1))						
						suma = 0
						prom = 0
						for i in total:
							suma += i.puntuacion
						prom = float(suma)/float(len(total))											
						detalle.puntuacion_total = int(round(prom))
						detalle.save()
						return redirect('/detalleArticulo/{}'.format(detalle.id))						
				else:
					carrito_usuario = Carrito.objects.get(usuario=request.user)			
					detalle.carrito.add(carrito_usuario)
					existe = Reserva.objects.filter(Q(producto_id = id) & Q(carrito_id = carrito_usuario.id))
					if existe:
						messages.error(request, 'Ya se reservó este artículo')
					else:
						carrito_usuario = Carrito.objects.get(usuario=request.user)			
						detalle.carrito.add(carrito_usuario)
						existencia= int(detalle.inventario.existencia)
						cantidad = request.POST.get('cantidad',None)
						cant=int(cantidad)

						if cant > existencia:
							messages.error(request, 'No se pudo realizar la reserva. Existencia del articulo: {}'.format(existencia))
						else:
							reserva=Reserva()
							reserva.carrito_id=carrito_usuario.id
							reserva.producto_id=id
							reserva.cantidad=cantidad
							reserva.save()
							messages.success(request, 'Se reservó el artículo {}'.format(detalle.nombre))

							#Restar existencia
							nueva_existencia=existencia-cant
							detalle.inventario.existencia=nueva_existencia
							detalle.inventario.save()
							return redirect('/detalleArticulo/{}'.format(detalle.id))

			except Carrito.DoesNotExist:
				carrito_usuario = Carrito()
				carrito_usuario.usuario = request.user
				carrito_usuario.save()
				detalle.carrito.add(carrito_usuario)
				existencia= int(detalle.inventario.existencia)
				cantidad = request.POST.get('cantidad',None)
				cant=int(cantidad)

				if cant > existencia:
					messages.error(request, 'No se pudo realizar la reserva. Existencia del articulo: {}'.format(existencia))
				else:
					reserva=Reserva()
					reserva.carrito_id=carrito_usuario.id
					reserva.producto_id=id
					reserva.cantidad=cantidad
					reserva.save()

					#Restar existencia
					nueva_existencia=existencia-cant
					detalle.inventario.existencia=nueva_existencia
					detalle.inventario.save()
					messages.success(request, 'Se reservo el articulo {}'.format(detalle.nombre))
				return redirect('/detalleArticulo/{}'.format(detalle.id))		
		return render(request,'cliente/detalleArticulo.html', contexto)
	except Valoracion.DoesNotExist:		
		valoracion = Valoracion()
		valoracion.puntuacion = 0
		valoracion.usuario = request.user
		valoracion.producto = detalle
		valoracion.save()
		detalle = Producto.objects.get(id=id)		
		contexto = {'art': detalle, 'puntuacion':0}
		return render(request,'cliente/detalleArticulo.html', contexto)
	except Producto.DoesNotExist:
		return render(request,'cliente/articulos.html',{'error':'No existe el producto solicitado'})


def paginacion_productos(request,articulos,elementos):
	paginator = Paginator(articulos, elementos)
	parametros = request.GET.copy()
	if parametros.has_key('page'):
		del parametros['page']
	
	page = request.GET.get('page')
	try:
		articulos = paginator.page(page)
	except PageNotAnInteger:
		articulos = paginator.page(1)
	except EmptyPage:
		articulos = paginator.page(paginator.num_pages)
	return {'art':articulos,'parametros':parametros}

def pre_orden(request):	
	try:
		carrito = Carrito.objects.get(usuario=request.user)
		reserva = Reserva.objects.filter(carrito = carrito)		
		if reserva:
			contexto = {'reserva':reserva}
			return render(request,'cliente/carrito.html',contexto)
		else:
			return render(request,'cliente/carrito.html',{'error':'No se han reservado articulos'})
	except Carrito.DoesNotExist:
		return render(request,'cliente/carrito.html',{'error':'No se han reservado articulos'})

def eliminar_pre(request, id):
	r = Reserva.objects.get(id=id)

	#Sumar existencia
	cantidad = int(r.cantidad)
	existencia = int(r.producto.inventario.existencia)
	r.producto.inventario.existencia = cantidad+existencia
	r.producto.inventario.save()

	r.delete()
	messages.success(request, 'Se eliminó de la pre-orden el articulo {}'.format(r.producto.nombre))
	return redirect('/preorden')

def editarReserva(request, id):
	res = Reserva.objects.get(id=id)
	if request.method == 'POST':
		existencia = int(res.producto.inventario.existencia)
		cant_res= int(res.cantidad)
		cantidad=request.POST.get('cantidad',None)
		cant=int(cantidad)
		existencia_real=existencia+cant_res

		if cant > existencia_real:
			messages.error(request, 'No se pudo realizar la reserva. Existencia del articulo: {}'.format(existencia))
		else:
			res.cantidad = cantidad
			res.save()
			messages.success(request, 'Se actualizó el artículo {}'.format(res.producto.nombre))

			#Restar existencia
			res.producto.inventario.existencia=existencia+cant_res-cant
			res.producto.inventario.save()
	else:
		context = {
			'res':res,
		}
		return render(request,"cliente/editarReserva.html", context)
		
	context = {
			'res':res,
		}
	return render(request,"cliente/editarReserva.html", context) 