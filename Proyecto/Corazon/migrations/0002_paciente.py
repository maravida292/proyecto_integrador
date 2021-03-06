# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-09 03:48
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Corazon', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Paciente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cedula', models.CharField(blank=True, max_length=10)),
                ('sexo', models.CharField(blank=True, choices=[('M', 'Mujer'), ('H', 'Hombre')], max_length=2)),
                ('edad', models.PositiveIntegerField(blank=True, null=True)),
                ('telefono', models.IntegerField(blank=True)),
                ('estado_civil', models.CharField(blank=True, choices=[('S', 'Solter@'), ('C', 'Casad@'), ('D', 'Divorsiad@'), ('V', 'Viud@')], max_length=2)),
                ('nacionalidad', models.CharField(blank=True, max_length=20)),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
