# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-19 21:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_auto_20151204_0416'),
    ]

    operations = [
        migrations.AddField(
            model_name='box',
            name='sort_order',
            field=models.IntegerField(null=True),
        ),
    ]
