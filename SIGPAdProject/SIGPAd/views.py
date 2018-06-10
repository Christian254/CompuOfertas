# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.models import User,Permission
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.views.defaults import page_not_found

from django.contrib.contenttypes.models import ContentType
from SIGPAd.models import *


# Create your views here.

def  iniciar_sesion(request):
	if request.method == 'POST':
		username = request.POST.get('usr', None)
		password = request.POST.get('pwd', None)
		user = authenticate(username=username, password=password)
		if user:
			login(request, user)
			if user.has_perm('SIGPAd.view_superuser'):
				return redirect('/indexAdministrador')
			elif user.has_perm('SIGPAd.view_seller'):
				return redirect('/indexVendedor')
			else:
				return redirect('/indexCliente')
		else:
			validar = "Credenciales erronéas."
			context = {'validar':validar}
			return render(request, 'LogIn.html', context)
	context = {}
	return render(request, 'LogIn.html', context)

@permission_required('SIGPAd.view_superuser')
def  indexAdministrador(request):
	return render_to_response('AdministradorTemplates/adminIndex.html')

@permission_required('SIGPAd.view_seller')
def  indexVendedor(request):
	return render_to_response('VendedorTemplates/vendedorIndex.html')


#Vista de los Clientes.
def registrarCliente(request):
	if request.method == 'POST':
		username = request.POST.get('usr', None)
		password = request.POST.get('pwd', None)
		password2 = request.POST.get('pwd2', None)
		user = authenticate(username=username, password=password, password2=password2)

		if user:
			validar = "Registro de usuario, ya existe."
			context = { 'validar':validar }
			return render(request, 'ClienteTemplates/registrarCliente.html', context)
		if password==password2:
			"""cliente = Cliente()
			cliente.nombre = request.POST.get('nombre', None)
			cliente.apellido = request.POST.get('apellido', None)
			cliente.sexo = request.POST.get('sexo', None)
			cliente.email = request.POST.get('correo', None)
			user = User.objects.create_user(username=username, password=password)
			content_type = ContentType.objects.get_for_model(Cliente)
			permission = Permission.objects.get(
				codename='view_client',
				content_type = content_type, 
			),
			user.user_permissions.add(permission)
			user.save()
			cliente.usuario = user
			cliente.save()
			return redirect('/indexCliente')
			"""
			cliente = Cliente()
			cliente.nombre = request.POST.get('nombre', None)
			cliente.apellido = request.POST.get('apellido', None)
			cliente.sexo = request.POST.get('sexo', None)
			cliente.email = request.POST.get('correo', None)
			user = User.objects.create_user(username=username, password=password)
			content_type = ContentType.objects.get_for_model(Cliente)
			permission = Permission.objects.get(
				codename='view_client',
				content_type=content_type,
				)
			user.user_permissions.add(permission)
			user.save()
			cliente.usuario = user
			cliente.save()
			return redirect('/registrarCliente')
		else:
			validar = "Las contraseñas son diferentes"
			context = { 'validar':validar }
			return render(request, 'ClienteTemplates/registrarCliente.html', context)
	context = {}
	return render(request, 'ClienteTemplates/registrarCliente.html', context)

def indexCliente(request):
	return render_to_response('ClienteTemplates/clienteIndex.html')

#Foro
def index(request):
	return render_to_response('index.html')


def handler404(request):
    return render(request, '404.html')