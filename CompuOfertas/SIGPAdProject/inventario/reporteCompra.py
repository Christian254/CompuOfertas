# -*- coding: ascii -*-
from __future__ import unicode_literals
import os
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, cm 
from reportlab.platypus import Paragraph, TableStyle,Table
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from django.http import HttpResponse
from datetime import time, date
from django.conf import settings
from reportlab.platypus import Image
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


def generar_reporte_compra(request, compra, detalle_compra):
	#Creando la cabecera HTTPResponse con PDF.
	response =HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = 'attachment; filename=factura_compra.pdf'
	#Creando el objeto PDF, usando el objeto BytesIO
	buffer = BytesIO()
	fecha= date.today()
	c = canvas.Canvas(buffer,pagesize=A4)

	#Cabecera
	cabecera(c)

	c.setLineWidth(.3)
	c.setFont('Helvetica',25)
	c.drawString(30,730,'CompuOfertas')
	#Se lee de izquierda a derecha y de abajo hacia arriba.

	c.setFont('Helvetica',12)
	c.drawString(480,750,fecha.strftime("%d-%m-%y"))
	c.line(460,747,560,747)

	#Letra
	pdfmetrics.registerFont(TTFont('Vera', 'Vera.ttf'))
	pdfmetrics.registerFont(TTFont('VeraBd', 'VeraBd.ttf'))
	pdfmetrics.registerFont(TTFont('VeraIt', 'VeraIt.ttf'))
	pdfmetrics.registerFont(TTFont('VeraBI', 'VeraBI.ttf'))


	c.setFont('VeraBd',15)
	c.drawString(30,680,'FACTURA DE COMPRA')

	#Table Header.
	styles = getSampleStyleSheet()
	styleBH = styles["Normal"]
	styleBH.alignment = TA_CENTER
	styleBH.fontSize = 9
	styleBH.fontName = "VeraBd"

	numero = Paragraph('''#''', styleBH)
	producto = Paragraph('''Producto''', styleBH)
	cantidad = Paragraph('''Cantidad''', styleBH)
	precio_compra = Paragraph('''Precio de Compra''', styleBH)
	descuento = Paragraph('''Descuento''', styleBH)

	data = []

	data.append([numero, producto, cantidad, precio_compra, descuento])


	detalles = [
		{'#':i+1, 'producto': det.producto.nombre, 'cantidad': det.cantidad,  'precio_compra': det.precio_compra, 'descuento': det.descuento}
		for i, det in enumerate(detalle_compra)
	]


	#Table
	styleN = styles["Normal"]
	styleN.alignment = TA_CENTER
	styleN.fontSize = 8
	styleN.fontName = "Vera"

	high = 650
        high = high - 25
        c.setFont('Vera',10)
        c.drawString(30,high,'Empleado: ' + compra.empleado.nombre.encode('utf-8').decode('utf-8'))
        high = high - 12
        c.setFont('Vera',10)
        c.drawString(30,high,'Proveedor: ' + str(compra.proveedor))
        high = high - 12
        c.setFont('Vera',10)
        c.drawString(30,high,'Descripcion: ' + compra.descripcion.encode('utf-8').decode('utf-8'))
        high = high - 12
        c.setFont('Vera',10)
        c.drawString(30,high,'Fecha y Hora: '+ str(compra.fecha_hora))
        high = high - 12
        
        high = 525
	for detalle in detalles:
		this_detalle = [detalle['#'], detalle['producto'], detalle['cantidad'], detalle['precio_compra'], detalle['descuento']]
		data.append(this_detalle)
		high = high - 12

	#Table size
	width, height = A4
	table = Table(data, colWidths=[1.2 * cm, 6.5 * cm, 4 * cm, 3 * cm, 3 * cm ])
	table.setStyle(TableStyle([ #Estilos de la tabla
		('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
		('BOX', (0, 0), (-1, -1), 0.25, colors.black), ]))

	#PDF size
	table.wrapOn(c, width, height)
	table.drawOn(c, 30,high)
        high = high - 25
        c.setFont('VeraBd',10)
        c.drawString(30,high,'Total de compra: ' + str(compra.total_compra))
        high = high - 12
        c.setFont('VeraBd',10)
        c.drawString(30,high,'Total de compra (con IVA): ' + str(compra.total_compra_iva))

	c.showPage() #Guardar pagina

	#Guardar PDF.

	c.save()

	#Obteniendo los valores de BytesIO buffer y escribiedo el reponse.
	pdf= buffer.getvalue()
	buffer.close()
	response.write(pdf)
	return response


def cabecera(pdf):
	imagen = settings.MEDIA_ROOT+'/logo.png'
	#imagen = settings.STATIC_URL+'imagenes/fiaOfertasLogo.png'
	pdf.drawImage(imagen, 40,750,120,90, preserveAspectRatio=True)
