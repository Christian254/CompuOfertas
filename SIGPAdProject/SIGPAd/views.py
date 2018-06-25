# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.models import User,Permission
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.views.defaults import page_not_found
from datetime import datetime

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

#Vista administrador.

@permission_required('SIGPAd.view_superuser')
def  indexAdministrador(request):
	return render_to_response('AdministradorTemplates/adminIndex.html')


@permission_required('SIGPAd.view_superuser')
def listadoDeEmpleados(request):
	empleados = Empleado.objects.all()
	context = {
		'empleados':empleados,
	}
	return render(request, 'AdministradorTemplates/empleados.html', context)

@permission_required('SIGPAd.view_superuser')
def  crearEmpleado(request):
	if request.method == 'POST':
		empleado = Empleado()
		cargo = Puesto.objects.get(nombre=request.POST.get('puestoEmpleado', None))
		empleado.puesto = cargo
		empleado.nombre = request.POST.get('nombre',None)
		empleado.apellido = request.POST.get('apellido',None)
		empleado.telefono = request.POST.get('telefono',None)
		empleado.fechaNac = request.POST.get('fecha_nacimiento',None)
		empleado.sexo = request.POST.get('sexo',None)
		empleado.email = request.POST.get('email',None)
		empleado.foto = request.FILES.get('foto',None)
		empleado.fecha_trabajo = request.POST.get('fecha_trabajo',None)
		empleado.dui = request.POST.get('dui',None)
		empleado.nit = request.POST.get('nit',None)
		empleado.afp = request.POST.get('afp',None)
		empleado.isss = request.POST.get('isss',None)
		empleado.save()

		puestos = Puesto.objects.all()
		exito = "Empleado guardado con éxito."
		context = {
			'cargo':cargo,
			'puestos':puestos,
			'exito':exito,
		}
		return render(request, 'AdministradorTemplates/crearEmpleado.html', context)
	puestos = Puesto.objects.all()
	context = {
		'puestos':puestos,
	}
	return render(request, 'AdministradorTemplates/crearEmpleado.html', context)

@permission_required('SIGPAd.view_superuser')
def crearUsuario(request):
	return render_to_response('AdministradorTemplates/crearUsuario.html')

@permission_required('SIGPAd.view_superuser')
def editarEmpleado(request, pk):
	mensaje = None
	existe = None
	try:
		empleado = Empleado.objects.get(empleado=pk)
	except Empleado.DoesNotExist:
		empleado = None
	if empleado is not None:
		puestos = Puesto.objects.all()
		empleado.fechaNac = empleado.fechaNac.strftime("%Y-%m-%d")
		empleado.fecha_trabajo = empleado.fecha_trabajo.strftime("%Y-%m-%d")
		if request.method == 'POST':
			cargo = Puesto.objects.get(nombre=request.POST.get('puestoEmpleado', None))
			empleado.puesto = cargo
			empleado.nombre = request.POST.get('nombre',None)
			empleado.apellido = request.POST.get('apellido',None)
			empleado.telefono = request.POST.get('telefono',None)
			empleado.fechaNac = request.POST.get('fecha_nacimiento',None)
			empleado.sexo = request.POST.get('sexo',None)
			empleado.email = request.POST.get('email',None)
			#empleado.foto = request.FILES.get('foto',None) 
			empleado.fecha_trabajo = request.POST.get('fecha_trabajo',None)
			empleado.dui = request.POST.get('dui',None)
			empleado.nit = request.POST.get('nit',None)
			empleado.afp = request.POST.get('afp',None)
			empleado.isss = request.POST.get('isss',None)
			empleado.save()
			return redirect("/empleados")
		else:
			context = {
				'puestos':puestos,
				'empleado':empleado,
				'mensaje':mensaje,
			}
		return render(request,"AdministradorTemplates/editarEmpleado.html", context) 

	else:
		existe = "El empledo no existe"
		context = {
			'empleado':empleado,
			'existe':existe,
			'mensaje':mensaje,
		}
		return render(request,"AdministradorTemplates/editarEmpleado.html", context) 


@permission_required('SIGPAd.view_superuser')
def eliminarEmpleado(request, pk):
	empleado = get_object_or_404(Empleado, empleado=pk)
	try:
		empleado.delete()
		mensaje = "Empleado eliminado"
		context = {
			'mensaje': mensaje,
		}
		return render_to_response('AdministradorTemplates/eliminarEmpleado.html', context)
	except (KeyError, empleado.DoesNotExist):
		#Aqui tiene que ir la pagina 404 correcta.
		return render(request, '404.html', {
		    	'error_message': "Empleado no eliminado",
		})
	else:
		return redirect('/indexAdministrador')


#Vistas vendedores.
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

def ingresarPuesto(request):
	if request.method == 'POST':
		puesto = Puesto()
		puesto.nombre = request.POST.get('nombre', None)
		puesto.salario = request.POST.get('salario', None)
		content_type = ContentType.objects.get_for_model(Puesto)
		puesto.save()
		return redirect('/ingresarPuesto')
	else:
		context = {}
		return render(request, 'PuestoTemplates/ingresarPuesto.html', context)
	return render_to_response('PuestoTemplates/ingresarPuesto.html')

def sancionarEmpleado(request):
	return render_to_response('AdministradorTemplates/sancionarEmpleado.html')

def gestionarEmpleado(request):
	return render_to_response('AdministradorTemplates/gestionarEmpleado.html')