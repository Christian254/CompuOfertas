# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from models import *

# Register your models here.

class EmpleadoAdmin(admin.ModelAdmin):
	list_display = ('usuario','imagen') 
admin.site.register(Empleado, EmpleadoAdmin)

class ClienteAdmin(admin.ModelAdmin):
	pass
admin.site.register(Cliente, ClienteAdmin)

class PuestoAdmin(admin.ModelAdmin):
	pass
admin.site.register(Puesto, PuestoAdmin)

class PlanillaAdmin(admin.ModelAdmin):
	pass
admin.site.register(Planilla, PlanillaAdmin)

class SancionAdmin(admin.ModelAdmin):
	pass
admin.site.register(Sancion, SancionAdmin)

class PagoAdmin(admin.ModelAdmin):
	pass
admin.site.register(Pago, PagoAdmin)

class HoraExtraAdmin(admin.ModelAdmin):
	pass
admin.site.register(HoraExtra, HoraExtraAdmin)

class CategoriaAdmin(admin.ModelAdmin):
	pass
admin.site.register(Categoria, CategoriaAdmin)

class DetalleCompraAdmin(admin.ModelAdmin):
	pass
admin.site.register(DetalleCompra, DetalleCompraAdmin)

class ProductoAdmin(admin.ModelAdmin):
	pass
admin.site.register(Producto, ProductoAdmin)

class CompraAdmin(admin.ModelAdmin):
	pass
admin.site.register(Compra, CompraAdmin)

class VentaAdmin(admin.ModelAdmin):
	pass
admin.site.register(Venta, VentaAdmin)

class InventarioAdmin(admin.ModelAdmin):
	pass
admin.site.register(Inventario, InventarioAdmin)

class DetalleVentaAdmin(admin.ModelAdmin):
	pass
admin.site.register(DetalleVenta, DetalleVentaAdmin)