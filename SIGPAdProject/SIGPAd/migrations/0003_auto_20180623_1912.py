# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-24 01:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('SIGPAd', '0002_auto_20180623_1857'),
    ]

    operations = [
        migrations.CreateModel(
            name='Puesto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=25)),
                ('salario', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
        ),
        migrations.AddField(
            model_name='empleado',
            name='puesto',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='SIGPAd.Puesto'),
        ),
    ]
