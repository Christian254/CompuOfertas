# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-10-21 19:37
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('emisor', models.CharField(max_length=70)),
                ('receptor', models.CharField(max_length=70)),
                ('chat', models.IntegerField(default=0)),
                ('conectado', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Mensaje',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.IntegerField(default=0)),
                ('fecha_hora', models.DateTimeField(default=datetime.datetime.now)),
                ('msj', models.CharField(max_length=300)),
                ('img', models.ImageField(blank=True, null=True, upload_to='img_producto')),
                ('chat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Foro.Chat')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='chat',
            unique_together=set([('emisor', 'receptor')]),
        ),
    ]
