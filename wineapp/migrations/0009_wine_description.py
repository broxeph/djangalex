# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-29 03:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wineapp', '0008_auto_20160128_2250'),
    ]

    operations = [
        migrations.AddField(
            model_name='wine',
            name='description',
            field=models.TextField(max_length=1000, null=True),
        ),
    ]