from __future__ import unicode_literals
from __future__ import absolute_import 

from django.conf.urls import url, handler404
from django.contrib import admin
from Foro.views import *
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

urlpatterns = [
	url(r'mensajes/$', login_required(mensajes), name="mensajes"),
]