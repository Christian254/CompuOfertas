# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-11-03 18:06
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Carrito',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_hora', models.DateTimeField(default=datetime.datetime.now)),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('emisor', models.CharField(max_length=70)),
                ('chat', models.IntegerField(default=0)),
                ('conectado', models.IntegerField(default=0)),
                ('estado', models.IntegerField(default=0)),
                ('ultimo', models.CharField(max_length=300)),
                ('receptor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Mensaje',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.IntegerField(default=0)),
                ('recibido', models.IntegerField(default=0)),
                ('enviado', models.IntegerField(default=1)),
                ('fecha_hora', models.DateTimeField(default=datetime.datetime.now)),
                ('msj', models.CharField(max_length=300)),
                ('img', models.ImageField(blank=True, null=True, upload_to='img_mensaje')),
                ('chat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Foro.Chat')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='chat',
            unique_together=set([('emisor', 'receptor')]),
        ),
    ]
