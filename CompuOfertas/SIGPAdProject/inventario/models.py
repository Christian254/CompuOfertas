# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from SIGPAd.models import *
from datetime import datetime

# Create your models here.

# Modelos del Sprint #2.
class Sucursal(models.Model):
    nombre_sucursal = models.CharField(max_length=20)
    ubicacion = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre_sucursal
    

class Inventario(models.Model):
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)
    precio_venta_producto = models.DecimalField(max_digits=6,decimal_places=2,default=0)
    precio_promedio_compra = models.DecimalField(max_digits=6,decimal_places=2,default=0)
    existencia = models.IntegerField(default=0)
    def natural_key(self):
        return (self.existencia, self.precio_venta_producto)

class Categoria(models.Model):
    codigo = models.CharField(max_length=10,unique=True)
    nombre = models.CharField(max_length=70,unique=True)
    descripcion = models.CharField(max_length=200)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    categoria = models.ForeignKey(Categoria,on_delete=models.CASCADE)
    inventario = models.ForeignKey(Inventario,on_delete=models.CASCADE)
    codigo = models.CharField(max_length=10,unique=True) ##lo dejare asi para que el id siga siendo el que proporciona django
    nombre = models.CharField(max_length=70)
    marca = models.CharField(max_length=30)
    descripcion = models.CharField(max_length=100)
    estado = models.IntegerField(default=1)
    img = models.ImageField(upload_to="img_producto", blank=True, null=True)

    def imagen(self):
        return format_html( "<image src='{}' style='height:100px' />".format(self.img.url) )

    def __str__(self):
        return self.nombre

#clase aun faltara a ponerla a prueba, se creara una nueva cada compra y venta
class Kardex(models.Model):
    fecha = models.DateField()
    cantEntrada = models.IntegerField()
    cantSalida = models.IntegerField()
    cantExistencia = models.IntegerField()
    precEntrada = models.DecimalField(max_digits=7,decimal_places=2)
    precSalida = models.DecimalField(max_digits=7,decimal_places=2)
    precExistencia = models.DecimalField(max_digits=10,decimal_places=2)
    montoEntrada =models.DecimalField(max_digits=20,decimal_places=2)
    montoSalida =models.DecimalField(max_digits=20,decimal_places=2)
    montoExistencia= models.DecimalField(max_digits=20,decimal_places=2)
    producto = models.ForeignKey(Producto,on_delete=models.CASCADE)


class Proveedor(models.Model):
    razon_social = models.CharField(max_length=256)
    nit = models.CharField(max_length=17)
    telefono = models.CharField(max_length=8)
    email = models.CharField(max_length=80)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.razon_social

class Compra(models.Model):
    empleado = models.ForeignKey('SIGPAd.Empleado', on_delete=models.SET_NULL, null=True)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.SET_NULL, null=True)
    total_compra= models.DecimalField(max_digits=10,decimal_places=2)
    iva_compra = models.DecimalField(max_digits=4,decimal_places=2)
    descripcion = models.CharField(max_length=100)
    fecha_hora = models.DateTimeField(default=datetime.now)

    def _strftime():
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

class DetalleCompra(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE) 
    cantidad = models.IntegerField(default=0)
    precio_unitario = models.DecimalField(max_digits=6,decimal_places=2)
    descuento = models.DecimalField(max_digits=6,decimal_places=2)
    precio_total = models.DecimalField(max_digits=6,decimal_places=2)

class Venta(models.Model):
    empleado = models.ForeignKey('SIGPAd.Empleado', on_delete=models.SET_NULL, null=True)
    cliente = models.ForeignKey('SIGPAd.Cliente', on_delete=models.SET_NULL, null=True)
    total_venta = models.DecimalField(max_digits=10, decimal_places=2)
    iva_venta = models.DecimalField(max_digits=4,decimal_places=2)
    descripcion = models.CharField(max_length=100)
    fecha_hora = models.DateTimeField()
    nombre_cliente = models.CharField(max_length=20,blank=True,null=True) #Cliente que llega a la tienda y no esta en el sistema.
    dui_cliente = models.CharField(max_length=10, blank=True, null=True) #Cliente que llega a la tienda y no esta en el sistema.

class DetalleVenta(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=0)
    precio_unitario = models.DecimalField(max_digits=6,decimal_places=2)
    descuento = models.DecimalField(max_digits=6,decimal_places=2)







