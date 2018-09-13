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
	url(r'registrarProducto/(?P<pk>\d+)/$', login_required(registrarProducto), name="registrarProducto"),
	url(r'mostrarProducto/(?P<pk>\d+)$', login_required(mostrarProducto), name="mostrarProducto"),
	url(r'editarProducto/(?P<pk>\d+)$', login_required(editarProducto), name="editarProducto"),
	url(r'eliminarProducto/(?P<pk>\d+)$', login_required(eliminarProducto), name="eliminarProducto"),
	url(r'productoEliminado/(?P<pk>\d+)$', login_required(productoEliminado), name="productoEliminado"),
	url(r'activarProducto/(?P<pk>\d+)$', login_required(activarProducto), name="activarProducto"),
	#Venta
	url(r'registrarVenta/$', login_required(registrarVenta), name="registrarVenta"),
	url(r'mostrarVenta/$', login_required(mostrarVenta), name="mostrarVenta"),
	url(r'^facturaVenta/(?P<id>\d+)$', login_required(facturaVenta), name="FacturaVenta"),
	#Servicios
	url(r'productoDisponible/$', login_required(productoDisponible), name="productoDisponible"),
	url(r'clienteRegistrado/$', login_required(clienteRegistrado), name="clienteRegistrado"),
	url(r'subirExcel/$', login_required(subirExcel), name="subirExcel"),
	#Compras
	url(r'listadoCompras/$',login_required(listado_de_compras), name="ListadoDeCompras"),
	url(r'nuevaCompra/$', login_required(nueva_compra), name="NuevaCompra"),
	#inventario
	url(r'mostrarInventario',login_required(mostrarInventario),name="mostrarInventario"),
]