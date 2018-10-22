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
# Create your views here.

#@permission_required('SIGPAd.es_cliente')
def mensajes(request,pk):
	user = request.user
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
			print("enviar: "+chat.receptor.username)
			if request.method == 'POST':
				c = request.POST.get('msg',None)
				chat.ultimo=c
				chat.save()
				mens = Mensaje(chat=chat,msj=c,enviado=user.id)
				mens.save()
	except Exception as e:
		print("no tiene usuarios o chat "+e.message)
	contexto={'usuarios':usersEmpleados,'clientes':userCliente,'contactos':contactos,'primer':primer,'chat':chat,'yo':user}
	return render(request,'cliente/mensajes.html',contexto)


def nuevoMensaje(request):
	user = request.user
	usersEmpleados = User.objects.filter(empleado__estado__gte=1).exclude(username=user.username)
	userCliente = User.objects.filter(cliente__estado__gte=1).exclude(username=user.username)
	contactos = User.objects.filter(chat__estado__gte=1).exclude(username=user.username)
	contexto={'usuarios':usersEmpleados,'clientes':userCliente,'contactos':contactos,'yo':user}
	return render(request,'cliente/nuevoMensaje.html',contexto)


def enviarNuevoMensaje(request, pk):
	user = request.user
	new_contactos = User.objects.get(pk=pk)
	if request.method=='POST':
		try:
			c = request.POST.get('msg',None)
			chat = Chat.objects.get(receptor=new_contactos,emisor=user.username)
			chat.ultimo=c
			chat.save()
			mens = Mensaje(chat=chat,msj=c,enviado=user.id)
			mens.save()
		except Chat.DoesNotExist:
			try:
				chat2 = Chat.objects.get(receptor=user,emisor=new_contactos.username)
				chat2.ultimo=c
				chat2.save()
				mens = Mensaje(chat=chat2,msj=c,enviado=user.id)
				mens.save()
			except Chat2.DoesNotExist:
				c = request.POST.get('msg',None)
				print(c)
				chat = Chat(emisor=user.username,receptor=new_contactos, conectado=1,estado=1,ultimo=c)
				chat.save()
				mens = Mensaje(chat=chat,msj=c,enviado=user.id)
				mens.save()

	contexto={'contactos':new_contactos,'yo':user}
	return render(request,'cliente/enviarNuevoMensaje.html',contexto)


def servicio_mensajeria(request,emisor_id,receptor_id):
	user = request.user
	if user.id==int(emisor_id) or user.id==int(receptor_id):
		mensajes = serializers.serialize("json",getChat(emisor_id,receptor_id,True),use_natural_foreign_keys=True)
	else:
		mensajes = serializers.serialize("json",[],use_natural_foreign_keys=True)
	return HttpResponse(mensajes, content_type='application/json')


def getChat(id_emisor,id_receptor,contactos):
	chat = None
	primer = None
	user = None
	try:
		primer = User.objects.get(pk=id_receptor)
		user = User.objects.get(pk=id_emisor)
		if contactos:
			chat =Chat.objects.all()
			chat=chat.filter(Q(receptor=primer,emisor=user.username)|Q(receptor=user,emisor=primer.username)).distinct().first()
			return chat.mensaje_set.all()
	except Exception as e:
		return []





