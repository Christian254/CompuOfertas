# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-08-19 21:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SIGPAd', '0004_auto_20180819_1341'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='nombre',
            field=models.CharField(max_length=70, unique=True),
        ),
    ]