# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from models import *

# Register your models here.
class KardexAdmin(admin.ModelAdmin):
	pass
admin.site.register(Kardex, KardexAdmin)


class ProveedorAdmin(admin.ModelAdmin):
	pass
admin.site.register(Proveedor, ProveedorAdmin)

class ValoracionAdmin(admin.ModelAdmin):
	pass
admin.site.register(Valoracion, ValoracionAdmin)

class ReservaAdmin(admin.ModelAdmin):
	pass
admin.site.register(Reserva, ReservaAdmin)
