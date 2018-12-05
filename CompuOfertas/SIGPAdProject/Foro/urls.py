from __future__ import unicode_literals
from __future__ import absolute_import 

from django.conf.urls import url, handler404
from django.contrib import admin
from Foro.views import *
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
	url(r'foro$', ForoIndex, name='ForoIndex'),
	url(r'mensajes/(?P<pk>\d+)$', login_required(mensajes), name="mensajes"),
	url(r'nuevoMensaje/$', login_required(nuevoMensaje), name="nuevoMensaje"),
	url(r'enviarNuevoMensaje/(?P<pk>\d+)$', login_required(enviarNuevoMensaje), name="enviarNuevoMensaje"),
	url(r'servicio_mensajeria/(?P<emisor_id>\d+)/(?P<receptor_id>\d+)$', login_required(servicio_mensajeria), name="servicio_mensajeria"),
	url(r'servicio_chat/$', login_required(servicio_chat), name="servicio_chat"),
	url(r'articulos/$',login_required(articulo), name="articulos"),
	url(r'editarClientes/$', login_required(editarClientes), name="editarClientes"),
	url(r'editarFotoCliente/(?P<pk>\d+)$', login_required(editarFotoCliente), name="editarFotoCliente"),
	url(r'detalleArticulo/(?P<id>\d+)$',login_required(detalleArticulo), name="detalleArticulo"),
	url(r'preorden/$',login_required(pre_orden), name="preOrdern"),
	url(r'eliminar_pre/(?P<id>\d+)$',login_required(eliminar_pre), name="eliminarPre"),
	url(r'editarReserva/(?P<id>\d+)$',login_required(editarReserva), name="editarReserva"),

	#Mensajeria
	url(r'mini_chat/(?P<receptor_id>\d+)$',login_required(get_servicio_mini_chat), name="ServicioMiniChat"),
	url(r'servicio_usuario/(?P<pk>\d+)$',login_required(get_servicio_usuario), name="ServicioUsuario"),
	url(r'nuevo_mensaje_mini_chat/(?P<id_enviado>\d+)$',login_required(nuevo_mensaje_mini_chat), name="NuevoMensajeMiniChat"),
	url(r'enviar_mensaje_mini_chat/(?P<id_emisor>\d+)/(?P<id_receptor>\d+)$',login_required(enviar_mensajes_mini_chat), name="EnviarMensajeMiniChat"),
	url(r'chat$',login_required(MiniChat), name="MiniChat"),
	url(r'foro_index_mensaje$', ForoIndexMensaje, name='ForoIndexMensaje'),
]