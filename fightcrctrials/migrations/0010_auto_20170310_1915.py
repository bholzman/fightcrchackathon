# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-03-10 19:15
from __future__ import unicode_literals

import datetime
import django.contrib.postgres.fields
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('fightcrctrials', '0009_auto_20170310_1851'),
    ]

    operations = [
        migrations.AddField(
            model_name='crctrial',
            name='category',
            field=models.CharField(default=datetime.datetime(2017, 3, 10, 19, 15, 26, 677649, tzinfo=utc), max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='crctrial',
            name='resources',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.URLField(max_length=300), null=True, size=None),
        ),
    ]