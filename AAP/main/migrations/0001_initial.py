# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-02-24 19:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Apartment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('link', models.URLField(db_index=True, max_length=300)),
                ('price', models.IntegerField(blank=True)),
                ('price_m2', models.IntegerField(blank=True)),
                ('date_time', models.DateTimeField(auto_now_add=True)),
                ('city', models.CharField(max_length=50)),
                ('agent', models.CharField(blank=True, max_length=300)),
                ('site', models.CharField(max_length=30)),
                ('address', models.CharField(max_length=300)),
                ('floor', models.CharField(blank=True, max_length=7)),
                ('living_space', models.FloatField(blank=True)),
                ('rooms', models.IntegerField(blank=True)),
                ('district', models.CharField(blank=True, max_length=50, null=True)),
                ('type_house', models.CharField(blank=True, max_length=20, null=True)),
                ('active', models.BooleanField()),
            ],
        ),
    ]
