# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-25 02:54
from __future__ import unicode_literals

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
            name='Cliente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=25)),
                ('apellido', models.CharField(max_length=25)),
                ('sexo', models.CharField(blank=True, max_length=10)),
                ('email', models.EmailField(max_length=70)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'permissions': (('es_cliente', 'Es Cliente'),),
            },
        ),
        migrations.CreateModel(
            name='Empleado',
            fields=[
                ('empleado', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=25)),
                ('apellido', models.CharField(max_length=25, null=True)),
                ('telefono', models.CharField(max_length=8, null=True)),
                ('fechaNac', models.DateField(null=True)),
                ('sexo', models.CharField(blank=True, max_length=10)),
                ('email', models.EmailField(max_length=70)),
                ('foto', models.ImageField(null=True, upload_to='fotos_empleados')),
                ('fecha_trabajo', models.DateField(null=True)),
                ('dui', models.CharField(max_length=10, null=True)),
                ('nit', models.CharField(max_length=17, null=True)),
                ('afp', models.CharField(max_length=12, null=True)),
                ('isss', models.CharField(max_length=9, null=True)),
            ],
            options={
                'permissions': (('view_superuser', 'Vista de SuperUsuario-Administrador'), ('view_seller', 'Vista de Vendedor'), ('view_accounter', 'Vista de Contador')),
            },
        ),
        migrations.CreateModel(
            name='Pago',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nomPago', models.CharField(max_length=30)),
                ('fecha_pago', models.DateField()),
                ('salarioBase', models.DecimalField(decimal_places=2, max_digits=8)),
                ('pagoafp', models.DecimalField(decimal_places=2, max_digits=8)),
                ('insaforp', models.DecimalField(decimal_places=2, max_digits=8)),
                ('vacaciones', models.DecimalField(decimal_places=2, max_digits=8)),
                ('aguinaldo', models.DecimalField(decimal_places=2, max_digits=8)),
                ('costomensual', models.DecimalField(decimal_places=2, max_digits=8)),
                ('empleado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SIGPAd.Empleado')),
            ],
        ),
        migrations.CreateModel(
            name='Planilla',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_pago_planilla', models.DateField()),
                ('nomPlanilla', models.CharField(max_length=30)),
                ('totalSalario', models.DecimalField(decimal_places=2, max_digits=8)),
                ('totalAFP', models.DecimalField(decimal_places=2, max_digits=8)),
                ('totalISSS', models.DecimalField(decimal_places=2, max_digits=8)),
                ('totalVacaciones', models.DecimalField(decimal_places=2, max_digits=8)),
                ('totalInsaforp', models.DecimalField(decimal_places=2, max_digits=8)),
                ('totalSalarioBase', models.DecimalField(decimal_places=2, max_digits=8)),
            ],
        ),
        migrations.CreateModel(
            name='Puesto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=25)),
                ('salario', models.DecimalField(decimal_places=2, max_digits=8)),
            ],
        ),
        migrations.CreateModel(
            name='Sancion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sancion', models.CharField(max_length=30)),
                ('descripcion', models.CharField(max_length=150)),
                ('descuento', models.DecimalField(decimal_places=2, max_digits=8)),
                ('fecha_sancion', models.DateField()),
                ('empleado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SIGPAd.Empleado')),
            ],
        ),
        migrations.AddField(
            model_name='pago',
            name='planilla',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SIGPAd.Planilla'),
        ),
        migrations.AddField(
            model_name='empleado',
            name='puesto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SIGPAd.Puesto'),
        ),
        migrations.AddField(
            model_name='empleado',
            name='usuario',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
