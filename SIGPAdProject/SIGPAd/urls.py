from __future__ import unicode_literals
from __future__ import absolute_import 

from django.conf.urls import url, handler404
from django.contrib import admin
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

app_name = 'SIGPAd'
admin.autodiscover()

urlpatterns = [
	url(r'^$', views.index, name='Index'),

	url(r'^login$', views.iniciar_sesion, name="LogIn"),
	url(r'indexAdministrador$', views.indexAdministrador, name="AdminIndex"),
	url(r'indexVendedor$', views.indexVendedor, name="VendedorIndex"),

	#URL Cliente.
	url(r'registrarCliente$', views.registrarCliente, name="RegistrarCliente"),
	url(r'indexCliente$', views.indexCliente, name="ClienteIndex")
]