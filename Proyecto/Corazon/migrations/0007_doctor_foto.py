# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-14 23:16
from __future__ import unicode_literals

import Corazon.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Corazon', '0006_auto_20160614_1039'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='foto',
            field=models.ImageField(blank=True, upload_to=Corazon.models.url),
        ),
    ]