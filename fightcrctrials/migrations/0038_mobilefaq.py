# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2018-11-07 02:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fightcrctrials', '0037_auto_20180623_1824'),
    ]

    operations = [
        migrations.CreateModel(
            name='MobileFAQ',
            fields=[
                ('faq_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='fightcrctrials.FAQ')),
            ],
            bases=('fightcrctrials.faq',),
        ),
    ]
