# -*- coding: utf-8 -*-
# Generated by Django 1.11.27 on 2021-01-04 02:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fightcrctrials', '0042_remove_crctrial_additional_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='crctrial',
            name='last_edited',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='crctrial',
            name='last_edited_by',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]