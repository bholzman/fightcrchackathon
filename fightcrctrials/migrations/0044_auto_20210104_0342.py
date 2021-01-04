# -*- coding: utf-8 -*-
# Generated by Django 1.11.27 on 2021-01-04 03:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fightcrctrials', '0043_auto_20210104_0243'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArchivedCRCTrial',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
            },
            bases=('fightcrctrials.crctrial',),
        ),
        migrations.AddField(
            model_name='crctrial',
            name='archived',
            field=models.BooleanField(default=False, verbose_name=b'Archived'),
        ),
    ]
