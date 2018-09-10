from __future__ import unicode_literals
from __future__ import absolute_import 

from django.conf.urls import url, handler404
from django.contrib import admin
from inventario.views import *
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
urlpatterns = [
    #URL Vendedor.
	url(r'indexVendedor$', login_required(indexVendedor), name="VendedorIndex"),
	url(r'registrarCategoria$', login_required(registrarCategoria), name="registrarCategoria"),
	url(r'ingresarProducto$', login_required(ingresarProducto), name="ingresarProducto"),
	url(r'registrarProducto/(?P<pk>\d+)$', login_required(registrarProducto), name="registrarProducto"),
	url(r'mostrarProducto/(?P<pk>\d+)$', login_required(mostrarProducto), name="mostrarProducto"),
	url(r'registrarVenta/$', login_required(registrarVenta), name="registrarVenta"),
	url(r'productoDisponible/$', login_required(productoDisponible), name="productoDisponible"),
	url(r'clienteRegistrado/$', login_required(clienteRegistrado), name="clienteRegistrado"),
	url(r'subirExcel/$', login_required(subirExcel), name="subirExcel"),
]