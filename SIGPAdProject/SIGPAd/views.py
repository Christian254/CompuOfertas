# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.models import User,Permission
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.views.defaults import page_not_found
from datetime import datetime
from decimal import *

from django.contrib.contenttypes.models import ContentType
from SIGPAd.models import *
from django.db import IntegrityError



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

def inicializarPuesto():
	try:
		puesto = Puesto.objects.all()
		i = len(puesto)
		if i==0:
			puesto = Puesto()
			puesto.nombre = "Gerente"
			puesto.salario = 2000.00
			puesto.save()
			puesto2 = Puesto()
			puesto2.nombre = "Vendedor"
			puesto2.salario = 600.00
			puesto2.save()
			puesto3 = Puesto()
			puesto3.nombre = "Contador"
			puesto3.salario = 300.00
			puesto3.save()
	except Exception as e:
		pass

@permission_required('SIGPAd.view_superuser')
def  indexAdministrador(request):
	inicializarPuesto()
	return render(request,'AdministradorTemplates/adminIndex.html',{})


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

	"""
	try:
		empleado = Empleado.objects.get(empleado=pk)
	except Empleado.DoesNotExist:
		empleado = None
	if empleado is not None:
		if empleado.puesto.nombre == "Vendedor":
			if request.method == 'POST':
				username = request.POST.get('usr', None)
				password = request.POST.get('pwd', None)
				password2 = request.POST.get('pwd2', None)
				user = authenticate(username=username, password=password, password2=password2)
				validarUser = username

				if user:
					validar = "Registro de usuario, ya existe."
					context = { 'validar':validar }
					return render(request, 'AdministradorTemplates/crearUsuario.html', context)
				else:
					if password == password2:
						user = User.objects.create_user(username=username, password=password)
						content_type = ContentType.objects.get_for_model(Empleado)
						permission = Permission.objects.get(
							codename='view_seller',
							content_type=content_type,
							)
						user.user_permissions.add(permission)
						user.save()
						empleado.usuario = user
						user.save()
						empleado.save()
						return redirect('/usuarios')
					else:

						validar = "Las contraseñas son diferentes"
						context = { 
						'validar':validar,  
						'empleado':empleado,}
						return render(request, 'AdministradorTemplates/crearUsuario.html', context)
	context = { 'empleado':empleado,}
	return render(request, 'AdministradorTemplates/crearUsuario.html', context)
	"""
	"""empleado = get_object_or_404(Empleado, empleado=pk)
	try:
    	# code that produces error
	except IntegrityError as e:
    	return render_to_response("AdministradorTemplates/crearUsuario.html", {"message": e.message})"""
@permission_required('SIGPAd.view_superuser')
def crearUsuario(request,pk):
	empleado = get_object_or_404(Empleado, empleado=pk)
	try:
		if empleado is not None:
			if empleado.puesto.nombre == "Vendedor":
				if request.method == 'POST':
					username = request.POST.get('usr', None)
					password = request.POST.get('pwd', None)
					password2 = request.POST.get('pwd2', None)
					user = authenticate(username=username, password=password, password2=password2)
					validarUser = username

					if user:
						validar = "Registro de usuario, ya existe."
						context = { 'validar':validar }
						return render(request, 'AdministradorTemplates/crearUsuario.html', context)
					else:
						if password == password2:
							user = User.objects.create_user(username=username, password=password)
							content_type = ContentType.objects.get_for_model(Empleado)
							permission = Permission.objects.get(
								codename='view_seller',
								content_type=content_type,
								)
							user.user_permissions.add(permission)
							user.save()
							empleado.usuario = user
							user.save()
							empleado.save()
							return redirect('/usuarios')
						else:

							validar = "Las contraseñas son diferentes"
							context = { 
							'validar':validar,  
							'empleado':empleado,}
							return render(request, 'AdministradorTemplates/crearUsuario.html', context)
	except (KeyError, IntegrityError):
		#Aqui tiene que ir la pagina 404 correcta.
		context = { 
			'empleado':empleado,
			'validar': "Empleado duplicado",
			}
		return render(request, 'AdministradorTemplates/crearUsuario.html',context)
	except Empleado.DoesNotExist:
		empleado = None
	else:
		context = { 'empleado':empleado,}
		return render(request, 'AdministradorTemplates/crearUsuario.html', context)


@permission_required('SIGPAd.view_superuser')
def listadoDeUsuarios(request):
	puestoVendedor = Puesto.objects.filter(nombre__contains="Vendedor")
	vendedorSinUser = Empleado.objects.filter(puesto=puestoVendedor,usuario__id=None)

	context = {
		'vendedorSinUser':vendedorSinUser,
	}
	return render(request, 'AdministradorTemplates/listadoUsuarios.html', context)


@permission_required('SIGPAd.view_superuser')
def editarEmpleado(request, pk):
	mensaje = None
	existe = None
	try:
		empleado = Empleado.objects.get(empleado=pk)
	except Empleado.DoesNotExist:
		empleado = None
	if empleado is not None:
		#puestos = Puesto.objects.all()
		puestos = Puesto.objects.exclude(id=empleado.puesto.id)
		empleado.fechaNac = empleado.fechaNac.strftime("%Y-%m-%d")
		empleado.fecha_trabajo = empleado.fecha_trabajo.strftime("%Y-%m-%d")
		empleados = Empleado.objects.exclude(sexo=empleado.sexo)
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
				'empleados':empleados,
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
def editarFotoEmpleado(request,pk):
	try:
		empleado = Empleado.objects.get(empleado=pk)
	except Empleado.DoesNotExist:
		empleado = None
	if empleado is not None:
		puestos = Puesto.objects.exclude(id=empleado.puesto.id)
		data = Empleado.objects.exclude(sexo=empleado.sexo)[0]
		empleado.fechaNac = empleado.fechaNac.strftime("%Y-%m-%d")
		empleado.fecha_trabajo = empleado.fecha_trabajo.strftime("%Y-%m-%d")
		if request.method == 'POST':
			empleado.foto = request.FILES.get('foto',None) 
			empleado.save()
			return redirect("/empleados")
		else:
			context = {
				'puestos':puestos,
				'empleado':empleado,
				'mensaje':mensaje,
				'data':data,
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
	user = request.user
	if user.is_authenticated():
		if user.is_superuser:
			return render(request,'AdministradorTemplates/adminIndex.html',{})
		else:
			return render(request,'VendedorTemplates/vendedorIndex.html',{})			
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
	user = request.user
	if user.is_authenticated():
		if user.is_superuser:
			return render(request,'AdministradorTemplates/adminIndex.html',{})
		else:
			return render(request,'VendedorTemplates/vendedorIndex.html',{})			
	return render_to_response('ClienteTemplates/clienteIndex.html')

#Foro
def index(request):
	user = request.user
	if user.is_authenticated():
		if user.is_superuser:
			return render(request,'AdministradorTemplates/adminIndex.html',{})
		else:
			return render(request,'VendedorTemplates/vendedorIndex.html',{})
	else:
		try:
			user = User.objects.all()
			i= len(user)
			if i==0:
				user = User.objects.create_superuser(username='admin', email='mh15012@ues.edu.sv',password= 'root')
				user.save()
		except Exception as e:
			pass
	return render(request,'index.html',{})


def planilla(request,idplanilla):	
	try:
		planilla = Planilla.objects.get(pk=idplanilla)
		pagos = Pago.objects.filter(planilla = planilla)
		anios = 0	
		for pago in pagos:	    	    
			empleado = Empleado.objects.get(pk=pago.empleado.empleado)
			pago.salarioBase = empleado.puesto.salario
			pago.pagoafp = round(empleado.puesto.salario * Decimal('0.0675'),2)
			pago.pagoisss = round(empleado.puesto.salario * Decimal('0.075'),2)
			pago.insaforp =  round(empleado.puesto.salario * Decimal('0.01'),2)
			pago.vacaciones = round(empleado.puesto.salario * Decimal('0.03'),2)
			pago.aguinaldo = 1
			pago.costomensual = 3
			pago.save() 

		pagos = Pago.objects.filter(planilla = planilla)

		return render(request,'AdministradorTemplates/planilla.html',{'pagos':pagos})
	except Exception as e:
		return render(request,'AdministradorTemplates/adminIndex.html',{})

def gestionarPlanilla(request):
	planilla = Planilla.objects.all()
	return render(request,'AdministradorTemplates/gestionarPlanilla.html',{'planilla':planilla})

def crearPlanilla(request):
	if request.method == 'POST':
		planilla = Planilla()
		planilla.nomPlanilla = request.POST.get('codigo',None)
		planilla.fecha_pago_planilla = request.POST.get('fecha',None)
		planilla.save()
		empleados = Empleado.objects.filter(estado=1)
		for i in empleados:
			nompago = i.apellido[0] + i.nombre[0] + str(i.empleado) + str(planilla.id)
			pago = Pago(planilla = planilla, empleado = i, nomPago = nompago, fecha_pago=planilla.fecha_pago_planilla)
			pago.save()
	return render(request,'AdministradorTemplates/crearPlanilla.html',{})

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