# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from SIGPAd.models import *
from datetime import datetime
from decimal import *

class Chat(models.Model):
	class Meta:
		unique_together = (('emisor'),('receptor'))
	emisor = models.CharField(max_length=70)
	receptor = models.CharField(max_length=70)
	chat = models.IntegerField(default=0)
	conectado = models.IntegerField(default=0)

class Mensaje(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    estado = models.IntegerField(default=0)
    fecha_hora = models.DateTimeField(default=datetime.now)
    msj = models.CharField(max_length=300)   
    img = models.ImageField(upload_to="img_producto", blank=True, null=True)

    def imagen(self):
        return format_html( "<image src='{}' style='height:100px' />".format(self.img.url) )

    def __str__(self):
        return self.msj

    def _strftime():
        return datetime.now().strftime('%d-%m-%Y %H:%M:%S')