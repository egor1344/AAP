# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-02 14:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_remove_apartment_street'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apartment',
            name='link',
            field=models.URLField(db_index=True, max_length=300),
        ),
    ]
