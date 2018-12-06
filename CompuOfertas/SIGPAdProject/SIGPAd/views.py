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
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType
from SIGPAd.models import *
from django.db import IntegrityError
from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import UpdateView, CreateView





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
				return redirect('/articulos')
		else:
			validar = "Credenciales erróneas."
			context = {'validar':validar}
			return render(request, 'exterior/foro.html', context)
	context = {}
	return render(request, 'exterior/foro.html', context)

#Vista administrador.


@permission_required('SIGPAd.view_superuser')
def inventarioGral(request):
	productos = Producto.objects.filter(estado=1)
	consulta = request.GET.get('consulta')
	if consulta:
		productos = productos.filter(
			Q(nombre_sucursal__icontains = consulta)|
			Q(ubicacion__icontains = consulta)
			).distinct()

	paginator = Paginator(productos, 1)
	parametros = request.GET.copy()
	if parametros.has_key('page'):
		del parametros['page']
	
	page = request.GET.get('page')
	try:
		productos = paginator.page(page)
	except PageNotAnInteger:
		productos = paginator.page(1)
	except EmptyPage:
		productos = paginator.page(paginator.num_pages)

	context={'productos':productos}
	return render(request,'AdministradorTemplates/inventarioGral.html',context)

def inicializarPuesto():
	try:
		puesto = Puesto.objects.all()
		i = len(puesto)
		if i==0:
			puesto = Puesto()
			puesto.nombre = "Gerente"
			puesto.salario = 2000.00
			puesto.save()
			puesto3 = Puesto()
			puesto3.nombre = "Contador"
			puesto3.salario = 300.00
			puesto3.save()
	except Exception as e:
		pass

@permission_required('SIGPAd.view_superuser')
def  indexAdministrador(request):
	return render(request,'AdministradorTemplates/adminIndex.html',{})


@permission_required('SIGPAd.view_superuser')
def listadoDeEmpleados(request):
	planilla=Planilla.objects.all()
	ultima=0	
	for p in planilla:
		ultima=p.id
	empleados_list = Empleado.objects.filter(estado=1)	
	consulta = request.GET.get('consulta')
	if consulta:
		empleados_list = empleados_list.filter(
			Q(nombre__icontains = consulta)|
			Q(apellido__icontains = consulta)|
			Q(puesto__nombre__icontains = consulta)
			).distinct()
	paginator = Paginator(empleados_list, 10) #Cambiar al numero que deseen que se muestre
	parametros = request.GET.copy()
	if parametros.has_key('page'):
		del parametros['page']
	
	page = request.GET.get('page')
	try:
		empleados = paginator.page(page)
	except PageNotAnInteger:
		empleados = paginator.page(1)
	except EmptyPage:
		empleados = paginator.page(paginator.num_pages)    
	context = {
		'empleados':empleados,'ultima':ultima, 'parametros':parametros
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

		#muy importante no eliminar por favor
		try:
			planilla=Planilla.objects.all()
			ultima=0
			for p in planilla:
				ultima=p.id
			pl = Planilla.objects.get(pk=ultima)
			nompago = empleado.apellido[0] + empleado.nombre[0] + str(empleado.empleado) + str(pl.id)
			pago = Pago(planilla = pl, empleado = empleado, nomPago = nompago, fecha_pago=pl.fecha_pago_planilla)
			pago.save()
		except Exception as e:
			exito=exito+" \n El empleado no pudo ser agregado a la planilla"


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

					if user:
						validar = "Registro de usuario, ya existe."
						context = { 'validar':validar }
						return render(request, 'AdministradorTemplates/crearUsuario.html', context)
					else:
						if password == password2:
							if len(password) < 8:
								validar = "tiene que tener minimo 8 caracteres"
								context = { 
								'validar':validar,  
								'empleado':empleado,}
								return render(request, 'AdministradorTemplates/crearUsuario.html', context)								
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
			elif empleado.puesto.nombre == "Gerente":
				if request.method == 'POST':
					username = request.POST.get('usr', None)
					password = request.POST.get('pwd', None)
					password2 = request.POST.get('pwd2', None)
					user = authenticate(username=username, password=password, password2=password2)

					if user:
						validar = "Registro de usuario, ya existe."
						context = { 'validar':validar }
						return render(request, 'AdministradorTemplates/crearUsuario.html', context)
					else:
						if password == password2:
							user = User.objects.create_user(username=username, password=password)
							content_type = ContentType.objects.get_for_model(Empleado)
							permission = Permission.objects.get(
								codename='view_superuser',
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
			elif empleado.puesto.nombre == "Contador":
				if request.method == 'POST':
					username = request.POST.get('usr', None)
					password = request.POST.get('pwd', None)
					password2 = request.POST.get('pwd2', None)
					user = authenticate(username=username, password=password, password2=password2)

					if user:
						validar = "Registro de usuario, ya existe."
						context = { 'validar':validar }
						return render(request, 'AdministradorTemplates/crearUsuario.html', context)
					else:
						if password == password2:
							user = User.objects.create_user(username=username, password=password)
							content_type = ContentType.objects.get_for_model(Empleado)
							permission = Permission.objects.get(
								codename='view_accounter',
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
			'validar': "Usuario duplicado",
			}
		return render(request, 'AdministradorTemplates/crearUsuario.html',context)
	except Empleado.DoesNotExist:
		empleado = None
	else:
		context = { 'empleado':empleado,}
		return render(request, 'AdministradorTemplates/crearUsuario.html', context)


@permission_required('SIGPAd.view_superuser')
def editarUsuario(request, pk):
	empleado = get_object_or_404(Empleado, empleado=pk)
	try:
		if empleado is not None:
			usuario = get_object_or_404(User, id=empleado.usuario.id)
			try:
				if request.method == 'POST':
					pwdAntigua = request.POST.get('pwdAntigua', None)
					verificacionPassword = check_password(pwdAntigua,usuario.password)
					if verificacionPassword:
						usr = request.POST.get('usr',None)
						pwdNueva = request.POST.get('pwdNueva', None)
						usuario.username = usr
						usuario.set_password(pwdNueva)
						usuario.save()
						context = { 
							'empleado':empleado,
							'usuario':usuario,
							'exito': "Usuario editado con éxito",
						}
						return render(request, 'AdministradorTemplates/editarUsuario.html',context)
					else:
						context = {
							'empleado':empleado,
							'validar':"Error, contraseña antigua incorrecta",
						}
						return 	render(request, 'AdministradorTemplates/editarUsuario.html',context)
			except (KeyError, IntegrityError):
				#Aqui tiene que ir la pagina 404 correcta.
				context = { 
					'empleado':empleado,
					'validar': "Usuario duplicado",
					}
				return render(request, 'AdministradorTemplates/crearUsuario.html',context)
			except(KeyError, usuario.DoesNotExist):
				context = { 
					'empleado':empleado,
					'validar': "Usuario no existe",
				}
				return render(request, 'AdministradorTemplates/editarUsuario.html',context)
	except Empleado.DoesNotExist:
		empleado = None
	else:
		context = { 'empleado':empleado,}
		return render(request, 'AdministradorTemplates/editarUsuario.html', context)

@permission_required('SIGPAd.view_superuser')
def eliminarUsuario(request, pk):
	empleado = get_object_or_404(Empleado, empleado=pk)
	try:
		if empleado is not None:
			usuario = get_object_or_404(User, id=empleado.usuario.id)
			try:
				empleado.usuario = None
				usuario.delete()
				context = {
					'mensaje':"Usuario eliminado",
				}
				return redirect('/usuarios')
			except (KeyError, usuario.DoesNotExist):
				return render(request, 'AdministradorTemplates/listadoUsuarios.html', {
				    	'error_message': "No selecciono un usuario valido a eliminar.",
				})			
	except (KeyError, empleado.DoesNotExist):
		return render(request, 'AdministradorTemplates/listadoUsuarios.html', {
		    	'error_message': "No selecciono un empleado valido a eliminar.",
		})
	else:
		return redirect('/usuarios')	


@permission_required('SIGPAd.view_superuser')
def listadoDeUsuarios(request):
	puestoGerente = Puesto.objects.filter(nombre__contains="Gerente")
	gerentesSinUser = Empleado.objects.filter(puesto=puestoGerente,usuario__id=None,estado=1)
	gerentes = Empleado.objects.filter(puesto=puestoGerente,estado=1).exclude(usuario__id=None)

	puestoVendedor = Puesto.objects.filter(nombre__contains="Vendedor")
	vendedoresSinUser = Empleado.objects.filter(puesto=puestoVendedor,usuario__id=None,estado=1)
	vendedores = Empleado.objects.filter(puesto=puestoVendedor,estado=1).exclude(usuario__id=None)

	puestoContador = Puesto.objects.filter(nombre__contains="Contador")
	contadoresSinUser = Empleado.objects.filter(puesto=puestoContador,usuario__id=None,estado=1)
	contadores = Empleado.objects.filter(puesto=puestoContador,estado=1).exclude(usuario__id=None)

	context = {
		'gerentesSinUser':gerentesSinUser,
		'gerentes':gerentes,
		'vendedoresSinUser':vendedoresSinUser,
		'vendedores':vendedores,
		'contadoresSinUser':contadoresSinUser,
		'contadores':contadores,
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
		try:
			puestos = Puesto.objects.exclude(id=empleado.puesto.id)
		except:
			puestos=Puesto.objects.all()
		empleado.fechaNac = empleado.fechaNac.strftime("%Y-%m-%d")
		empleado.fecha_trabajo = empleado.fecha_trabajo.strftime("%Y-%m-%d")
		empleados = Empleado.objects.exclude(sexo=empleado.sexo)
		if empleado.sexo == "Femenino":
			otro = "Masculino"
		else:
			otro = "Femenino"
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
				'otro':otro,
			}
		return render(request,"AdministradorTemplates/editarEmpleado.html", context) 

	else:
		existe = "El empleado no existe"
		context = {
			'empleado':empleado,
			'existe':existe,
			'mensaje':mensaje,
			'otro':otro,
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
			return render(request, 'exterior/registrar_cliente.html', context)
		if password==password2:
			cliente = Cliente()
			cliente.nombre = request.POST.get('nombre', None)
			cliente.apellido = request.POST.get('apellido', None)
			cliente.sexo = request.POST.get('sexo', None)
			cliente.email = request.POST.get('correo', None)
			user = User.objects.create_user(username=username, password=password)
			content_type = ContentType.objects.get_for_model(Cliente)
			permission = Permission.objects.get(
				codename='es_cliente',
				content_type=content_type,
				)
			user.user_permissions.add(permission)
			user.save()
			cliente.usuario = user
			cliente.save()
			context = {
				'exito':"Éxito al registrarte, ingresa ubicandote en la página principal",
			}
			return render(request, 'exterior/registrar_cliente.html', context)
		else:
			validar = "Las contraseñas son diferentes"
			context = { 'validar':validar }
			return render(request, 'exterior/registrar_cliente.html', context)
	context = {}
	return render(request, 'exterior/registrar_cliente.html', context)

def indexCliente(request):
	user = request.user
	if user.is_authenticated():
		if user.is_superuser:
			return render(request,'AdministradorTemplates/adminIndex.html',{})
		else:
			return render(request,'ClienteTemplates/clienteIndex.html',{})			
	return render(request,'ClienteTemplates/clienteIndex.html',{})

#Foro
def index(request):
	user = request.user
	if user.is_authenticated():
		if user.is_superuser:
			return render(request,'AdministradorTemplates/adminIndex.html',{})
		else:
			empleado = Empleado.objects.filter(usuario=user)
			if len(empleado) > 0:
				return render(request,'VendedorTemplates/vendedorIndex.html',{})
			else:
				return redirect('/articulos')
	else:
		try:
			user = User.objects.all()
			i= len(user)
			if i==0:
				inicializarPuesto()
				user = User.objects.create_superuser(username='admin', email='mh15012@ues.edu.sv',password= 'root1234')
				user.save()
				puesto = Puesto()
				puesto.nombre = "Vendedor"
				puesto.salario = 600.00
				puesto.save()
				empleado=Empleado(puesto=puesto,nombre='walter',apellido='marroquin',telefono='7777777',sexo='Masculino',email='walter@hotmail.com',dui='123',nit='1234',afp='34556',isss='1234')
				vendedor = User.objects.create_user(username='vendedor', password='root1234')
				content_type = ContentType.objects.get_for_model(Empleado)
				permission = Permission.objects.get(
					codename='view_seller',
					content_type=content_type,
					)
				vendedor.user_permissions.add(permission)
				empleado.usuario = vendedor
				vendedor.save()
				empleado.save()

		except Exception as e:
			pass

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
				return redirect('/articulos')
		else:
			validar = "Credenciales erróneas."
			context = {'validar':validar}
			return render(request, 'exterior/foro.html', context)
	context = {}
	return render(request, 'exterior/foro.html', context)


def planilla(request,idplanilla):

	try:		
		planilla = Planilla.objects.get(pk=idplanilla)
		pagos = Pago.objects.filter(planilla = planilla)
		planilla.totalAFP = 0
		planilla.totalISSS = 0
		planilla.totalVacaciones=0
		planilla.totalInsaforp=0
		planilla.totalSalarioBase =0
		planilla.totalAguinaldo = 0
		planilla.costomensual= 0
		planilla.totalHoras = 0
		planilla.save()
		horaestrasss = 0
		for pago in pagos:	    	    
			empleado = Empleado.objects.get(pk=pago.empleado.empleado)
			anio = empleado.fecha_trabajo.year
			anioActual = datetime.now().year
			anioTrabajado = anioActual - anio			
			pago.salarioBase = empleado.puesto.salario
			pago.pagoafp = round(empleado.puesto.salario * Decimal('0.0675'),2)
			pago.pagoisss = round(empleado.puesto.salario * Decimal('0.075'),2)
			pago.insaforp =  round(empleado.puesto.salario * Decimal('0.01'),2)
			var=((empleado.puesto.salario/30)*15*Decimal('1.3'))
			var2=(((empleado.puesto.salario/30)*15)*Decimal('0.1425'))
			pago.vacaciones=round((var+var2)/12,2)
			

			if anioTrabajado < 1:
				dias=0
				pago.aguinaldo=round((((empleado.puesto.salario/30)*0)/12),2)
				
			elif anioTrabajado >= 1 and anioTrabajado < 3:
				dias=10
				pago.aguinaldo=round((((empleado.puesto.salario/30)*10)/12),2)
			
			if (anioTrabajado >= 3 and anioTrabajado < 10):
				dias=15
				pago.aguinaldo=round((((empleado.puesto.salario/30)*dias)/12),2)
			elif (anioTrabajado >= 10):
				dias=18
				pago.aguinaldo=round((((empleado.puesto.salario/30)*dias)/12),2)
				

				
			horaE=0
			hora=HoraExtra.objects.filter(planilla=planilla, empleado=empleado)
			for h in hora:
				horaE=horaE+h.cantidad
			horaEx=horaE*2

			pago.totalHoraExtra=horaEx
			horaestrasss = horaestrasss + horaEx
			pago.costomensual = 3
			pago.save()
			planilla.totalAFP = round(Decimal(planilla.totalAFP) + Decimal(pago.pagoafp),2)
			planilla.totalISSS = round(Decimal(planilla.totalISSS) + Decimal(pago.pagoisss),2)
			planilla.totalVacaciones= round(Decimal(planilla.totalVacaciones)+Decimal(pago.vacaciones),2)
			planilla.totalInsaforp= round(Decimal(planilla.totalInsaforp)+Decimal(pago.insaforp),2)
			planilla.totalSalarioBase = round(Decimal(planilla.totalSalarioBase) + Decimal(pago.salarioBase),2)
			planilla.totalAguinaldo = round(Decimal(planilla.totalAguinaldo) + Decimal(pago.aguinaldo),2)
			planilla.totalHoras = horaEx
			planilla.save()
			planilla.costomensual=round( Decimal(planilla.totalSalarioBase) + Decimal(planilla.totalAguinaldo) + Decimal(planilla.totalInsaforp) + Decimal(planilla.totalVacaciones) + Decimal(planilla.totalISSS) + Decimal(planilla.totalAFP) ,2)
			planilla.save() 
		pagos = Pago.objects.filter(planilla = planilla)
		return render(request,'AdministradorTemplates/planilla.html',{'pagos':pagos,'planilla':planilla, 'hora':horaestrasss})
	except Exception as e:
		raise e
		return render(request,'AdministradorTemplates/adminIndex.html',{})

def reporte(request,pk):
	planilla = Planilla.objects.get(pk=pk)

	return generar_reporte(request, planilla)

def reporteDespido(request):
	empleado = Empleado.objects.filter(estado=0)

	return generar_reporte_despido(request, empleado)

def gestionarPlanilla(request):
	planilla = Planilla.objects.all()
	paginator = Paginator(planilla, 5)
	page = request.GET.get('page')
	try:
		planilla = paginator.page(page)
	except PageNotAnInteger:
		planilla = paginator.page(1)
	except EmptyPage:
		planilla = paginator.page(paginator.num_pages) 

	return render(request,'AdministradorTemplates/gestionarPlanilla.html',{'planilla':planilla})

def crearPlanilla(request):
	if request.method == 'POST':
		try:		
			planilla = Planilla()
			planilla.nomPlanilla = request.POST.get('codigo',None)
			planilla.fecha_pago_planilla = request.POST.get('fecha',None)
			planilla.save()
			empleados = Empleado.objects.filter(estado=1)
			for i in empleados:
				nompago = i.apellido[0] + i.nombre[0] + str(i.empleado) + str(planilla.id)
				pago = Pago(planilla = planilla, empleado = i, nomPago = nompago, fecha_pago=planilla.fecha_pago_planilla)
				pago.save()
			return render(request,'AdministradorTemplates/crearPlanilla.html',{'alerta': 'Se creó la planilla: '+planilla.nomPlanilla})
		except Exception as e:
			return render(request,'AdministradorTemplates/crearPlanilla.html',{'error':'Error al crear planilla'})
	else:
		return render(request,'AdministradorTemplates/crearPlanilla.html',{})

def horasExtra(request, idempleado, idplanilla):
	alerta=False
	if request.method == 'POST':
		horasExtra = HoraExtra()
		horasExtra.cantidad = request.POST.get('cantidad',None)
		horasExtra.fecha = request.POST.get('fecha',None)
		horasExtra.empleado=Empleado.objects.get(pk=idempleado)
		try:
			horasExtra.planilla=Planilla.objects.get(pk=idplanilla)
			horasExtra.save()
			return render(request,'AdministradorTemplates/horasExtra.html',{'alerta': 'Se ingresaron horas extras:'})
		except Exception as e:
			return render(request,'AdministradorTemplates/horasExtra.html',{'error':'Error al ingresar horas extras'})

	return render(request,'AdministradorTemplates/horasExtra.html',{})


def handler404(request):
    return render(request, '404.html')

def ingresarPuesto(request):
	if request.method == 'POST':
		try:
			puesto = Puesto()
			puesto.nombre = request.POST.get('nombre', None)
			puesto.salario = request.POST.get('salario', None)
			content_type = ContentType.objects.get_for_model(Puesto)
			puesto.save()			
			return render(request, 'PuestoTemplates/ingresarPuesto.html', {'alerta':'Se creó el puesto: '+puesto.nombre})
		except Exception as e:
			context = {'error':'Error, puesto inválido'}
			return render(request, 'PuestoTemplates/ingresarPuesto.html', context)
	else:
		context = {}
		return render(request, 'PuestoTemplates/ingresarPuesto.html', context)
	return render_to_response('PuestoTemplates/ingresarPuesto.html')

def gestionarPuesto(request):
	puesto=Puesto.objects.all()
	context={'puesto':puesto}
	return render(request,'PuestoTemplates/gestionarPuesto.html',context)

def sancionarEmpleado(request,pk):
	empleado = get_object_or_404(Empleado, empleado=pk)
	if request.method == 'POST':
		sancion = Sancion()
		sancion.sancion = request.POST.get('sancion', None)
		sancion.descripcion = request.POST.get('descripcion', None)
		sancion.fecha_sancion = datetime.now()
		try:
			sancion.empleado = empleado
			sancion.save()
		except Exception as e:
			return render(request,'AdministradorTemplates/sancionarEmpleado.html',{'error':'Empleado no existe'})		
	context = {
		'empleado':empleado,
	}
	return render(request,'AdministradorTemplates/sancionarEmpleado.html',context)

def gestionarEmpleado(request):
	return render_to_response('AdministradorTemplates/gestionarEmpleado.html')


@permission_required('SIGPAd.view_superuser')
def editarPuesto(request, pk):
	mensaje = None
	existe = None
	try:
		puesto = Puesto.objects.get(pk=pk)
	except Puesto.DoesNotExist:
		puesto = None

	if puesto is not None:
		print ("dentroif")	
		'''
		#puestos = Puesto.objects.all()
		empleado.fechaNac = empleado.fechaNac.strftime("%Y-%m-%d")
		empleado.fecha_trabajo = empleado.fecha_trabajo.strftime("%Y-%m-%d")
		puesto = Puesto.objects.exclude(sexo=empleado.sexo)
		'''
		if request.method == 'POST':
			print ("dentro")
			puesto.nombre = request.POST.get('nombre',None)
			puesto.salario = request.POST.get('salario',None)
			puesto.save()
			return redirect("/gestionarPuesto")
		else:
			context = {
				'puesto':puesto,
				'mensaje':mensaje,

			}
		return render(request,"PuestoTemplates/editarPuesto.html", context) 

	else:
		existe = "El puesto no existe"
		context = {
			'puesto':puesto,
			'existe':existe,
			'mensaje':mensaje,
		}
		return render(request,"PuestoTemplates/editarPuesto.html", context)

@permission_required('SIGPAd.view_superuser')
def eliminarPuesto(request, pk):
	puesto = get_object_or_404(Puesto, pk=pk)
	try:
		empleados=Empleado.objects.filter(puesto=puesto)
		for e in empleados:
			e.puesto=None
			e.save()
		puesto.delete()
		mensaje = "Puesto eliminado"
		context = {
			'mensaje': mensaje,
		}
		return redirect('/gestionarPuesto')
	except (KeyError, puesto.DoesNotExist):
		#Aqui tiene que ir la pagina 404 correcta.
		return render(request, '404.html', {
		    	'error_message': "Puesto no eliminado",
		})
	else:
		return redirect('/gestionarPuesto')

def gestionarSancion(request):
	sancion=Sancion.objects.all()
	context={'sancion':sancion}
	return render(request,'AdministradorTemplates/gestionarSancion.html',context)

@permission_required('SIGPAd.view_superuser')
def despedir(request, pk):
	try:
		empleado=Empleado.objects.get(empleado=pk)
		empleado.estado=0
		empleado.save()
		return redirect("/empleados")
	except Exception as e:
		return render(request,'AdministradorTemplates/empleados.html',context)

@permission_required('SIGPAd.view_superuser')
def confirmarDespido(request, pk):
	empleado = get_object_or_404(Empleado, empleado=pk)
	context = {
		'empleado': empleado,
	}
	return render(request, 'AdministradorTemplates/confirmarDespido.html', context)

@permission_required('SIGPAd.view_superuser')
def listadoDespedidos(request):
	empleados = Empleado.objects.filter(estado=0)
	context = {
		'empleados':empleados,
	}
	return render(request, 'AdministradorTemplates/despidos.html', context)

@permission_required('SIGPAd.view_superuser')
def eliminarDespedido(request, pk):
	empleado = get_object_or_404(Empleado, empleado=pk)
	try:
		if empleado is not None:
			empleado.delete()
			context = {
					'mensaje':"Empleado eliminado",
			}
			return redirect('/despedidos')
	except (KeyError, empleado.DoesNotExist):
		return render(request, 'AdministradorTemplates/despidos.html', {
		    	'error_message': "No selecciono un empleado valido a eliminar.",
		})
	else:
		return redirect('/despedidos')