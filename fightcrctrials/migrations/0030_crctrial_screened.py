# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-11-21 22:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fightcrctrials', '0029_crctrial_conditions'),
    ]

    operations = [
        migrations.AddField(
            model_name='crctrial',
            name='screened',
            field=models.NullBooleanField(default=None),
        ),
    ]