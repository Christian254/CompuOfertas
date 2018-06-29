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


def generar_reporte_despido(request, empleado):
	#Creando la cabecera HTTPResponse con PDF.
	response =HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = 'attachment; filename=Despedidos.pdf'
	
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
	c.drawString(30,680,'LISTADO DE EMPLEADOS DESPEDIDOS')

	#Table Header.
	styles = getSampleStyleSheet()
	styleBH = styles["Normal"]
	styleBH.alignment = TA_CENTER
	styleBH.fontSize = 9
	styleBH.fontName = "VeraBd"

	numero = Paragraph('''#''', styleBH)
	nombre = Paragraph('''Nombre''', styleBH)
	apellido = Paragraph('''Apellido''', styleBH)
	dui = Paragraph('''DUI''', styleBH)
	nit = Paragraph('''NIT''', styleBH)
	puesto = Paragraph('''Puesto''', styleBH)

	data = []

	data.append([numero, nombre, apellido, dui, nit, puesto])


	despedidos = [
		{'#':i+1, 'nombre': des.nombre, 'apellido': des.apellido,  'dui': des.dui, 'nit': des.nit, 'puesto': des.puesto.nombre}
		for i, des in enumerate(empleado)
	]


	#Table
	styleN = styles["Normal"]
	styleN.alignment = TA_CENTER
	styleN.fontSize = 8
	styleN.fontName = "Vera"

	high = 650
	for despedido in despedidos:
		this_despedido = [despedido['#'], despedido['nombre'], despedido['apellido'], despedido['dui'], despedido['nit'], despedido['puesto']]
		data.append(this_despedido)
		high = high - 18

	#Table size
	width, height = A4
	table = Table(data, colWidths=[1.2 * cm, 4 * cm, 4 * cm, 3 * cm, 3 * cm, 3 * cm])
	table.setStyle(TableStyle([ #Estilos de la tabla
		('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
		('BOX', (0, 0), (-1, -1), 0.25, colors.black), ]))

	#PDF size
	table.wrapOn(c, width, height)
	table.drawOn(c, 30,high)

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
