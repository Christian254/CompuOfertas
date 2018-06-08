from django.conf.urls import url
from django.contrib.auth.views import login
from . import views

app_name = 'sigpad'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/', login ,{'template_name': 'login.html'}, name="login"),   
]