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

def generar_reporte(request, planilla):
	#Creando la cabecera HTTPResponse con PDF.
	response =HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = 'attachment; filename=Planilla.pdf'
	
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

	#Table Header.
	styles = getSampleStyleSheet()
	styleBH = styles["Normal"]
	styleBH.alignment = TA_CENTER
	styleBH.fontSize = 7

	numero = Paragraph('''#''', styleBH)
	nombre = Paragraph('''Nombre''', styleBH)
	apellido = Paragraph('''Apellido''', styleBH)
	puesto = Paragraph('''Puesto''', styleBH)
	salarioBase = Paragraph('''Salario Base''', styleBH)
	horasExtras = Paragraph('''Horas Extra''', styleBH)
	isss = Paragraph('''ISSS''', styleBH)
	afp = Paragraph('''AFP''', styleBH)
	insaforp = Paragraph('''INSAFORP''', styleBH)
	vacaciones = Paragraph('''Vacaciones''', styleBH)
	aguinaldo = Paragraph('''Aguinaldo''', styleBH)

	data = []

	data.append([numero, nombre, apellido, puesto, salarioBase, horasExtras, isss, afp, insaforp, vacaciones, aguinaldo])

	p = [
		{'#':i+1, 'nombre': ut.empleado.nombre, 'apellido': ut.empleado.apellido, 'puesto':ut.empleado.puesto.nombre, 'salarioBase':ut.salarioBase,'horasExtras':ut.totalHoraExtra,'isss':ut.pagoisss,'afp':ut.pagoafp,'insaforp':ut.insaforp,'vacaciones':ut.vacaciones,'aguinaldo':ut.aguinaldo}
		for i, ut in enumerate(planilla.pago_set.all())		
	]
	p.append({'#':' ', 'nombre': ' ', 'apellido': '', 'puesto':' ', 'salarioBase':' ','horasExtras':' ','isss':' ','afp':' ','insaforp':' ' ,'vacaciones':' ','aguinaldo':' '})
	p.append({'#':' ', 'nombre': 'planilla:', 'apellido': planilla.nomPlanilla, 'puesto':'Totales', 'salarioBase':planilla.totalSalarioBase,'horasExtras':planilla.totalHoras,'isss':planilla.totalISSS,'afp':planilla.totalAFP,'insaforp':planilla.totalInsaforp,'vacaciones':planilla.totalVacaciones,'aguinaldo':planilla.totalAguinaldo})
	p.append({'#':' ', 'nombre': ' ', 'apellido': '', 'puesto':' ', 'salarioBase':' ','horasExtras':' ','isss':' ','afp':' ','insaforp':' ' ,'vacaciones':' ','aguinaldo':' '})
	p.append({'#':' ', 'nombre': 'planilla:', 'apellido': planilla.nomPlanilla, 'puesto':'Total', 'salarioBase':' ','horasExtras':' ','isss':' ','afp':' ','insaforp':' ','vacaciones':' ','aguinaldo':planilla.costomensual})
	

	#Table
	styleN = styles["BodyText"]
	styleN.alignment = TA_CENTER
	styleN.fontSize = 10

	high = 650
	for util in p:
		this_utilidad = [util['#'], util['nombre'], util['apellido'], util['puesto'], util['salarioBase'], util['horasExtras'], util['isss'], util['afp'], util['insaforp'], util['vacaciones'], util['aguinaldo']]
		data.append(this_utilidad)
		high = high - 18


	#Table size
	width, height = A4
	table = Table(data, colWidths=[0.5 * cm, 1.75 * cm, 1.75 * cm, 1.75 * cm, 1.75 * cm, 1.75 * cm,1.75 * cm,1.75 * cm,1.75 * cm,1.75 * cm,1.75 * cm])
	table.setStyle(TableStyle([ #Estilos de la tabla
		('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
		('BOX', (0, 0), (-1, -1), 0.25, colors.black), ]))

	#PDF size
	table.wrapOn(c, width, height)
	table.drawOn(c, 30,high)
	#++++)



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

