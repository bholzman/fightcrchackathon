# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-03-10 18:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fightcrctrials', '0005_crctrial'),
    ]

    operations = [
        migrations.AddField(
            model_name='crctrial',
            name='approved',
            field=models.BooleanField(default=False),
        ),
    ]
