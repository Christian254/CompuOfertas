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
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.

#@permission_required('SIGPAd.es_cliente')
def mensajes(request,pk):
	user = request.user
	error = ''
	usersEmpleados = User.objects.filter(empleado__estado__gte=1).exclude(username=user.username)
	userCliente = User.objects.filter(cliente__estado__gte=1).exclude(username=user.username)
	chats = Chat.objects.filter(receptor=user) 
	chats2 = Chat.objects.filter(emisor=user.username)
	print(chats)
	print(chats2)
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
		if contactos:
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
			error = "Para enviar un nuevo mensaje tiene que buscar el usuario en \"add contact\""
	contexto={'usuarios':usersEmpleados,'clientes':userCliente,'contactos':contactos,'primer':primer,'chat':chat,'yo':user,'error':error}
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


def servicio_mensajeria(request,emisor_id,receptor_id):
	user = request.user
	if user.id==int(emisor_id) or user.id==int(receptor_id):
		mensajes = serializers.serialize("json",getChat(emisor_id,receptor_id,True,user.id),use_natural_foreign_keys=True)
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
			chat =Chat.objects.all()
			chat=chat.filter(Q(receptor=primer,emisor=user.username)|Q(receptor=user,emisor=primer.username)).distinct().first()
			c = chat.mensaje_set.all().filter(estado=0).exclude(enviado=id)
			for x in c:
				x.estado=1
				x.save()
			print(c)
			return c
	except Exception as e:
		return []


def servicio_chat(request):
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
				datos.append({"model":"Foro.mensaje","pk":m.id,"fields":{"ids":m.id,"msj":m.msj,"username":x.emisor,"enviado":m.enviado}})
	for x in chats2:
		m1 = x.mensaje_set.all().filter(estado=0)
		val = len(m1)
		if val > 0 :
			m = m1.latest("id")
			if m.enviado != user.id:
				datos.append({"model":"Foro.mensaje","pk":m.id, "fields":{"ids":m.id,"msj":m.msj,"username":x.receptor.username,"enviado":m.enviado}})
	return datos

def articulo(request):
	articulos = Producto.objects.filter(inventario__existencia__gte=1).exclude(Q(inventario__precio_venta_producto=0) & Q(img__isnull=True)).exclude(img='')
	contexto = paginacion_productos(request,articulos,6)
	return render(request, 'cliente/articulos.html', contexto)

def detalleArticulo(request, id):
	detalle = Producto.objects.get(id=id)
	contexto = {'art': detalle}
	return render(request,'cliente/detalleArticulo.html', contexto)

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


