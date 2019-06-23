# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from SIGPAd.models import *
from datetime import datetime
from decimal import *
from Foro.models import Carrito

# Create your models here.

# Modelos del Sprint #2.0    

class Inventario(models.Model):
    precio_venta_producto = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    precio_promedio_compra = models.DecimalField(max_digits=8,decimal_places=2,default=0)
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
    carrito = models.ManyToManyField(Carrito, blank=True)
    codigo = models.CharField(max_length=10,unique=True) ##lo dejare asi para que el id siga siendo el que proporciona django
    nombre = models.CharField(max_length=70,unique=True)
    marca = models.CharField(max_length=30)
    descripcion = models.CharField(max_length=100)
    estado = models.IntegerField(default=1) 
    estadoForo = models.BooleanField(default=False)
    puntuacion_total = models.IntegerField(default=0)
    img = models.ImageField(upload_to="img_producto", blank=True, null=True)

    def imagen(self):
        return format_html( "<image src='{}' style='height:100px' />".format(self.img.url) )

    def __str__(self):
        return self.nombre

class Valoracion(models.Model):
    puntuacion = models.IntegerField(default=0)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)

class Reserva(models.Model):
    carrito = models.ForeignKey(Carrito,on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto,on_delete=models.CASCADE)
    cantidad= models.IntegerField(default=0)
    fecha_hora = models.DateTimeField(default=datetime.now)

#clase aun faltara a ponerla a prueba, se creara una nueva cada compra y venta
class Kardex(models.Model):
    fecha = models.DateField(blank=False,auto_now_add=True, auto_now=False)
    cantEntrada = models.IntegerField()
    cantSalida = models.IntegerField()
    cantExistencia = models.IntegerField()
    precEntrada = models.DecimalField(max_digits=8,decimal_places=2)
    precSalida = models.DecimalField(max_digits=8,decimal_places=2)
    precExistencia = models.DecimalField(max_digits=9,decimal_places=2)
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
    total_compra= models.DecimalField(max_digits=20,decimal_places=2)
    total_compra_iva = models.DecimalField(max_digits=20,decimal_places=2)
    descripcion = models.CharField(max_length=100)
    fecha_hora = models.DateTimeField(default=datetime.now)

    def _strftime():
        return datetime.now().strftime('%d-%m-%Y %H:%M:%S')

class DetalleCompra(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE) 
    cantidad = models.IntegerField(default=0)
    precio_compra = models.DecimalField(max_digits=10,decimal_places=2)
    descuento = models.DecimalField(max_digits=8,decimal_places=2)

    def save(self, *args, **kwargs):
        kards = Kardex.objects.filter(producto=self.producto)
        k = 0
        for x in kards:
            k=x.id
        kardex = Kardex()
        kardex.fecha = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        kardex.cantEntrada = self.cantidad
        kardex.cantSalida = 0
        kardex.cantExistencia = self.cantidad
        kardex.precEntrada = self.precio_compra
        kardex.precSalida = 0
        kardex.precExistencia = self.precio_compra
        kardex.montoEntrada = Decimal(self.cantidad) * Decimal(self.precio_compra)
        kardex.montoSalida=0
        kardex.montoExistencia = Decimal(self.cantidad) * Decimal(self.precio_compra)
        kardex.producto=self.producto
        prod = self.producto
        inv = prod.inventario
        inv.precio_promedio_compra=Decimal(self.precio_compra)
        inv.save()
        print(inv.precio_promedio_compra)
        kardex.save()
        if k > 0:
            ultimo = Kardex.objects.get(pk=k)
            cant = Decimal(kardex.cantExistencia) + Decimal(ultimo.cantExistencia)
            monto = Decimal(kardex.montoExistencia) + Decimal(ultimo.montoExistencia)
            kardex.cantExistencia = cant
            kardex.montoExistencia = monto
            kardex.precExistencia = monto / cant
            kardex.save()
            inv.precio_promedio_compra=kardex.precExistencia
            inv.save()
            print(inv.precio_promedio_compra)
        return super(DetalleCompra,self).save(*args,**kwargs)

class Venta(models.Model):
    empleado = models.ForeignKey('SIGPAd.Empleado', on_delete=models.SET_NULL, null=True)
    cliente = models.ForeignKey('SIGPAd.Cliente', on_delete=models.SET_NULL, null=True)
    total_venta = models.DecimalField(max_digits=20, decimal_places=2)
    iva_venta = models.DecimalField(max_digits=4,decimal_places=2)
    descripcion = models.CharField(max_length=100)
    fecha_hora = models.DateTimeField(default=datetime.now)
    nombre_cliente = models.CharField(max_length=20,blank=True,null=True) #Cliente que llega a la tienda y no esta en el sistema.
    dui_cliente = models.CharField(max_length=10, blank=True, null=True) #Cliente que llega a la tienda y no esta en el sistema.

class DetalleVenta(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=0)
    precio_unitario = models.DecimalField(max_digits=8,decimal_places=2)
    descuento = models.DecimalField(max_digits=7,decimal_places=2)
    total = models.DecimalField(max_digits=20,decimal_places=2)
