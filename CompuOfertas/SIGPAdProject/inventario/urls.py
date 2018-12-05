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
	#URL Categoria
	url(r'registrarCategoria$', login_required(registrarCategoria), name="registrarCategoria"),
	url(r'editarCategoria/(?P<pk>\d+)$', login_required(editarCategoria), name="editarCategoria"),
	url(r'eliminarCategoria/(?P<pk>\d+)$', login_required(eliminarCategoria), name="eliminarCategoria"),
	url(r'categoriaEliminada/$', login_required(categoriaEliminada), name="categoriaEliminada"),
	url(r'activarCategoria/(?P<pk>\d+)$', login_required(activarCategoria), name="activarCategoria"),
	#URL Proveedor
	url(r'registrarProveedores$', login_required(registrarProveedores), name="registrarProveedores"),
	url(r'editarProveedores/(?P<pk>\d+)/$', login_required(editarProveedores), name="editarProveedores"),
	url(r'eliminarProveedores/(?P<pk>\d+)$', login_required(eliminarProveedores), name="eliminarProveedores"),
	url(r'proveedoresEliminados/$', login_required(proveedoresEliminados), name="proveedoresEliminados"),
	url(r'activarProveedores/(?P<pk>\d+)$', login_required(activarProveedores), name="activarProveedores"),
	#URL Cliente
	url(r'registrarClientes$', login_required(registrarClientes), name="registrarClientes"),
	url(r'editarClientes/(?P<pk>\d+)/$', login_required(editarClientes), name="editarClientes"),
	url(r'eliminarClientes/(?P<pk>\d+)$', login_required(eliminarClientes), name="eliminarClientes"),
	url(r'clientesEliminados/$', login_required(clientesEliminados), name="clientesEliminados"),
	url(r'activarClientes/(?P<pk>\d+)$', login_required(activarClientes), name="activarClientes"),
	#URL Producto
	url(r'ingresarProducto$', login_required(ingresarProducto), name="ingresarProducto"),
	url(r'registrarProducto/(?P<pk>\d+)/$', login_required(registrarProducto), name="registrarProducto"),
	url(r'mostrarProducto/(?P<pk>\d+)$', login_required(mostrarProducto), name="mostrarProducto"),
	url(r'editarProducto/(?P<pk>\d+)$', login_required(editarProducto), name="editarProducto"),
	url(r'eliminarProducto/(?P<pk>\d+)$', login_required(eliminarProducto), name="eliminarProducto"),
	url(r'productoEliminado/(?P<pk>\d+)$', login_required(productoEliminado), name="productoEliminado"),
	url(r'activarProducto/(?P<pk>\d+)$', login_required(activarProducto), name="activarProducto"),
	url(r'productoAMostrar/$', login_required(productoAMostrar), name="productoAMostrar"),
	#Venta
	url(r'registrarVenta/$', login_required(registrarVenta), name="registrarVenta"),
	url(r'mostrarVenta/$', login_required(mostrarVenta), name="mostrarVenta"),
	url(r'^facturaVenta/(?P<id>\d+)$', login_required(facturaVenta), name="FacturaVenta"),
	url(r'mostrarReservas/$', login_required(mostrarReservas), name="mostrarReservas"),
	url(r'eliminarReserva/(?P<id>\d+)$',login_required(eliminarReserva), name="eliminarReserva"),
	url(r'aceptarReserva/(?P<id>\d+)$',login_required(aceptarReserva), name="aceptarReserva"),
	#Servicios
	url(r'productoDisponible/$', login_required(productoDisponible), name="productoDisponible"),
	url(r'clienteRegistrado/$', login_required(clienteRegistrado), name="clienteRegistrado"),
	url(r'subirExcel/$', login_required(subirExcel), name="subirExcel"),
	#Compras
	url(r'listadoCompras/$',login_required(listado_de_compras), name="ListadoDeCompras"),
	url(r'nuevaCompra/$', login_required(nueva_compra), name="NuevaCompra"),
	url(r'cancelarCompra/$', login_required(cancelar_compra), name="CancelarCompra"),
	url(r'facturarCompra/(?P<id>\d+)$', login_required(facturar_compra), name="FacturarCompra"),
	url(r'reporteCompra/(?P<id>\d+)$', login_required(reporte_compra), name="ReporteCompra"),
	#inventario
	url(r'mostrarInventario',login_required(mostrarInventario),name="mostrarInventario"),
	url(r'descargarInventario',login_required(descargarInventario),name="descargarInventario"),

	url(r'grafica$', login_required(grafica), name="grafica"),
	url(r'graficaMes$', login_required(graficaMes), name="graficaMes"),
	url(r'graficaEmpleado$', login_required(graficaEmpleado), name="graficaEmpleado"),
	url(r'graficaProducto$', login_required(graficaProducto), name="graficaProducto"),
	
	url(r'^mostrarKardex/(?P<pk>\d+)$', login_required(mostrarKardex), name="mostrarKardex"),
	#Perfil Vendedor
	url(r'^PerfilVendedor/$', login_required(editar_perfil_vendedor), name="PerfilVendedor"),
	#url(r'^editarFotoVendedor/(?P<pk>\d+)$', login_required(editar_foto_vendedor), name="EditarFotoVendedor"),
]