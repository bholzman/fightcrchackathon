# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-03-17 13:37
from __future__ import unicode_literals

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fightcrctrials', '0024_scriptruns'),
    ]

    operations = [
        migrations.AddField(
            model_name='crctrial',
            name='drug_brand_names',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=300), blank=True, null=True, size=None),
        ),
    ]