# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime
from decimal import *
from django.db import models
from django.conf import settings
from django.db.models import Count
from django.utils import timezone
from .models import *

def nuevoKardex(opcion,producto_id ,cantidad, precio):
	try:
		op = int(opcion)
		producto = Producto.objects.get(pk=int(producto_id))
		kards = Kardex.objects.filter(producto=producto)
		k = 0
		for x in kards:
			k = x.id
		kardex = Kardex()
		kardex.fecha = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
		retornar = False
		if op == 1:
			kardex.cantEntrada = cantidad
			kardex.cantSalida = 0
			kardex.cantExistencia = cantidad
			kardex.precEntrada = Decimal(precio)
			kardex.precSalida = 0
			kardex.precExistencia = precio
			kardex.montoEntrada = Decimal(cantidad) * Decimal(precio)
			kardex.montoSalida=0
			kardex.montoExistencia = Decimal(cantidad) * Decimal(precio)
			kardex.producto=producto
			kardex.save()
			if k > 0:
				ultimo = Kardex.objects.get(pk=k)
				cant = kardex.cantExistencia + ultimo.cantExistencia
				monto = kardex.montoExistencia + ultimo.montoExistencia
				kardex.cantExistencia = cant
				kardex.montoExistencia = monto
				kardex.precExistencia = monto / cant
				kardex.save()
			print("se anadio exitosamente el producto")
			retornar = True
		elif op == 2:
			if k > 0:
				ultimo = Kardex.objects.get(pk=k)
				if cantidad <= ultimo.cantExistencia:
					kardex.cantEntrada = 0
					kardex.cantSalida = cantidad
					kardex.cantExistencia = 0
					kardex.precEntrada = 0
					kardex.precSalida = ultimo.precExistencia
					kardex.precExistencia = ultimo.precExistencia
					kardex.montoEntrada = 0
					montoS = Decimal(cantidad) * Decimal(ultimo.precExistencia)
					kardex.montoSalida = montoS
					kardex.montoExistencia = 0
					kardex.producto=producto
					kardex.save()
					cant = ultimo.cantExistencia - cantidad  
					monto = ultimo.montoExistencia - montoS
					kardex.cantExistencia = cant
					kardex.montoExistencia = monto
					kardex.precExistencia = monto / cant
					kardex.save()
					print("se anadio exitosamente al kardex")
					retornar = True
				else:
					print("No existe kardex anterior al kardex")
					retornar = False
			else:
				print("Operacion fallida")
				retornar = False
		return retornar
	except Exception as e:
		print (e.message)
		return False