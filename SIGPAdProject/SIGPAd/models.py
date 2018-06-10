# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _


# Create your models here.
class Empleado(models.Model):
	usuario = models.ForeignKey(User, on_delete=models.CASCADE)
	nombre=models.CharField(max_length=25)
	apellido=models.CharField(max_length=25)
	sexo = models.CharField(max_length=10, blank=True)
	email=models.EmailField(max_length=70)

	def __str__(self):
		return self.nombre

	class Meta:
		permissions = (
          ('view_superuser', 'Vista de SuperUsuario-Administrador'),
          ('view_seller', 'Vista de Vendedor'),
          ('view_accounter', 'Vista de Contador'),
        )

class Cliente(models.Model):
	usuario = models.ForeignKey(User, on_delete=models.CASCADE)
	nombre=models.CharField(max_length=25)
	apellido=models.CharField(max_length=25)
	sexo = models.CharField(max_length=10, blank=True)
	email=models.EmailField(max_length=70)

	def __str__(self):
		return self.nombre

	class Meta:
		permissions = (
			('es_cliente', _('Es Cliente')),
		)
		