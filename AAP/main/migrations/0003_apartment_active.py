# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-02 09:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20161002_0847'),
    ]

    operations = [
        migrations.AddField(
            model_name='apartment',
            name='active',
            field=models.BooleanField(default=1),
            preserve_default=False,
        ),
    ]