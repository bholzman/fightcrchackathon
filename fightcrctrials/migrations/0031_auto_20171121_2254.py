# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-11-21 22:54
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fightcrctrials', '0030_crctrial_screened'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='crctrial',
            options={'permissions': (('phase_1', 'Phase 1 reviewer'),)},
        ),
    ]
