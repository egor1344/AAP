# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-02 08:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='apartment',
            name='district',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='apartment',
            name='type_house',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
