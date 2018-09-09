# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from models import *

# Register your models here.

class SucursalAdmin(admin.ModelAdmin):
	list_display = ('nombre_sucursal','ubicacion') 
admin.site.register(Sucursal, SucursalAdmin)