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

	url(r'^login$', iniciar_sesion, name="LogIn"),
	url(r'^logout/$',auth_views.logout, {'next_page':'/login'}, name='logout'),
	url(r'indexAdministrador$', login_required(indexAdministrador), name="AdminIndex"),
	url(r'indexVendedor$', login_required(indexVendedor), name="VendedorIndex"),

	#URL Cliente.
	url(r'registrarCliente$', registrarCliente, name="RegistrarCliente"),
	url(r'indexCliente$', login_required(indexCliente), name="ClienteIndex")
]