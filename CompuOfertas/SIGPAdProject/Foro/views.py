# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.models import User,Permission
from django.contrib.auth.hashers import check_password
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.views.defaults import page_not_found
# Create your views here.
@permission_required('SIGPAd.es_cliente')
def mensajes(request):
	user = request.user
	usersEmpleados = User.objects.filter(empleado__estado__gte=1).exclude(username=user.username)
	contexto={'usuarios':usersEmpleados}
	return render(request,'cliente/mensajes.html',contexto)