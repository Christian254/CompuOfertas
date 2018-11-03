# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from models import *

# Register your models here.

class CarritoAdmin(admin.ModelAdmin):
	list_display = ('usuario','fecha_hora') 
admin.site.register(Carrito, CarritoAdmin)