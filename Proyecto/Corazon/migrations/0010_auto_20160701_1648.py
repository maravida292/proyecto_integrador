# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-01 21:48
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Corazon', '0009_auto_20160618_1026'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='paciente',
            options={'permissions': (('ver_perfil', 'Pueden ver su perfil'),)},
        ),
    ]
