from __future__ import unicode_literals
from __future__ import absolute_import 

from django.conf.urls import url, handler404
from django.contrib import admin
from SIGPAd.views import *
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

app_name = 'SIGPAd'
admin.autodiscover()


urlpatterns = [
	url(r'^$', index, name='Index'),

	url(r'^login/$', iniciar_sesion, name="LogIn"),
	url(r'^logout/$',auth_views.logout, {'next_page':'/login'}, name='logout'),
	#URL Administrador.
	url(r'indexAdministrador$', login_required(indexAdministrador), name="AdminIndex"),
	url(r'empleados$', login_required(listadoDeEmpleados), name="Empleados"),
	url(r'ingresarNuevoEmpleado$', login_required(crearEmpleado), name="NuevoEmpleado"),
	url(r'^eliminarEmpleado/(?P<pk>\d+)$', login_required(eliminarEmpleado), name="EliminarEmpleado"),
	url(r'^editarEmpleado/(?P<pk>\d+)$', login_required(editarEmpleado), name="EditarEmpleado"),
	url(r'^editarFotoEmpleado/(?P<pk>\d+)$', login_required(editarFotoEmpleado), name="EditarFotoEmpleado"),
	url(r'^planilla/(?P<idplanilla>\d+)$', login_required(planilla), name="planilla"),
	url(r'^horasExtra/(?P<idempleado>\d+)/(?P<idplanilla>\d+)$', login_required(horasExtra), name="horasExtra"),
	url(r'^crearPlanilla$',login_required(crearPlanilla), name="crearPlanilla"),

	url(r'usuarios$', login_required(listadoDeUsuarios), name="Usuarios"),
	url(r'ingresarNuevoUsuario/(?P<pk>\d+)$', login_required(crearUsuario), name="NuevoUsuario"),
	url(r'editarUsuario/(?P<pk>\d+)$', login_required(editarUsuario), name="EditarUsuario"),
	url(r'eliminarUsuario/(?P<pk>\d+)$', login_required(eliminarUsuario), name="EliminarUsuario"),
	url(r'^reporte/(?P<pk>\d+)$', login_required(reporte), name="reporte"),
	url(r'^despedir/(?P<pk>\d+)$', login_required(despedir), name="despedir"),
	url(r'^confirmarDespido/(?P<pk>\d+)$', login_required(confirmarDespido), name="ConfirmarDespido"),
	url(r'despedidos$', login_required(listadoDespedidos), name="Despedidos"),
	url(r'eliminarDespedido/(?P<pk>\d+)$', login_required(eliminarDespedido), name="EliminarDespedido"),
	url(r'^reporteDespido/$', login_required(reporteDespido), name="ReporteDeDespido"),
	url(r'^inventarioGral/$',login_required(inventarioGral),name="inventarioGral"),



	#URL Cliente.
	url(r'registrarCliente$', registrarCliente, name="RegistrarCliente"),
	url(r'indexCliente$', login_required(indexCliente), name="ClienteIndex"),

	url(r'ingresarPuesto$', ingresarPuesto, name="IngresarPuesto"),
	url(r'gestionarPuesto$', gestionarPuesto, name="GestionarPuesto"),
	url(r'sancionarEmpleado/(?P<pk>\d+)$', sancionarEmpleado, name="SancionarEmpleado"),
	url(r'gestionarEmpleado$', gestionarEmpleado, name="GestionarEmpleado"),
	url(r'gestionarPlanilla$', gestionarPlanilla, name="GestionarPlanilla"),
	url(r'^editarPuesto/(?P<pk>\d+)$', login_required(editarPuesto), name="EditarPuesto"),
	url(r'^eliminarPuesto/(?P<pk>\d+)$', login_required(eliminarPuesto), name="EliminarPuesto"),
	url(r'gestionarSancion$', login_required(gestionarSancion), name="GestionarSancion"),
]