# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-05-09 14:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='text',
            field=models.TextField(default=''),
        ),
    ]
