# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils.html import format_html
from django.utils.translation import ugettext as _


# Create your models here.
class Puesto(models.Model):
	nombre=models.CharField(max_length=25, unique=True)
	salario=models.DecimalField(max_digits=8, decimal_places=2)
	
	def __str__(self):
		return self.nombre

class Empleado(models.Model):
	empleado = models.AutoField(primary_key=True)
	usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	puesto = models.ForeignKey(Puesto, on_delete=models.CASCADE)
	nombre = models.CharField(max_length=25)
	apellido = models.CharField(max_length=25, null=True)
	telefono = models.CharField(max_length=8, null=True)
	fechaNac = models.DateField(auto_now=False, auto_now_add=False, null=True)
	sexo = models.CharField(max_length=10, blank=True)
	email = models.EmailField(max_length=70)
	foto = models.ImageField(upload_to="fotos_empleados", null=True)
	fecha_trabajo = models.DateField(auto_now=False, auto_now_add=False,null=True)
	dui = models.CharField(max_length=10)
	nit = models.CharField(max_length=17)
	afp=models.CharField(max_length=12)
	isss = models.CharField(max_length=9)
	def __str__(self):
		return self.nombre

	def imagen(self):
		return format_html( "<image src='{}' style='height:100px' />".format(self.foto.url) )

	class Meta:
		permissions = (
          ('view_superuser', 'Vista de SuperUsuario-Administrador'),
          ('view_seller', 'Vista de Vendedor'),
          ('view_accounter', 'Vista de Contador'),
        )

class Planilla(models.Model):
	fecha_pago_planilla=models.DateField(auto_now=False, auto_now_add=False)
	nomPlanilla=models.CharField(max_length=30)
	totalAFP=models.DecimalField(max_digits=8, decimal_places=2)
	totalISSS=models.DecimalField(max_digits=8, decimal_places=2)
	totalVacaciones=models.DecimalField(max_digits=8, decimal_places=2)
	totalInsaforp=models.DecimalField(max_digits=8, decimal_places=2)
	totalSalarioBase=models.DecimalField(max_digits=8, decimal_places=2)
	costomensual=models.DecimalField(max_digits=8, decimal_places=2)
	def __str__(self):
		return self.nomPlanilla

class Pago(models.Model):
	planilla=models.ForeignKey(Planilla, on_delete=models.CASCADE)
	empleado=models.ForeignKey(Empleado, on_delete=models.CASCADE)
	nomPago=models.CharField(max_length=30)
	fecha_pago=models.DateField(auto_now=False, auto_now_add=False)
	salarioBase=models.DecimalField(max_digits=8, decimal_places=2)
	pagoafp=models.DecimalField(max_digits=8, decimal_places=2)
	insaforp=models.DecimalField(max_digits=8, decimal_places=2)
	vacaciones=models.DecimalField(max_digits=8, decimal_places=2)
	aguinaldo=models.DecimalField(max_digits=8, decimal_places=2)
	totalSalario=models.DecimalField(max_digits=8, decimal_places=2)

	def __str__(self):
		return self.nomPago


class Cliente(models.Model):
	usuario = models.ForeignKey(User, on_delete=models.CASCADE)
	nombre = models.CharField(max_length=25)
	apellido = models.CharField(max_length=25)
	sexo = models.CharField(max_length=10, blank=True)
	email = models.EmailField(max_length=70)

	def __str__(self):
		return self.nombre

	class Meta:
		permissions = (
			('es_cliente', _('Es Cliente')),
		)

class Sancion(models.Model):
	empleado=models.ForeignKey(Empleado, on_delete=models.CASCADE)
	sancion=models.CharField(max_length=30)
	descripcion=models.CharField(max_length=150)
	descuento=models.DecimalField(max_digits=8, decimal_places=2)
	fecha_sancion=models.DateField(auto_now=False, auto_now_add=False)

	def __str__(self):
		return self.sancion


		