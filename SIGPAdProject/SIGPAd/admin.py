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

