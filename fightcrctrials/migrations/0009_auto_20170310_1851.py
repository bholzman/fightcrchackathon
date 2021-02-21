# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-03-10 18:51
from __future__ import unicode_literals

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fightcrctrials', '0008_auto_20170310_1834'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='crctrial',
            name='publications',
        ),
        migrations.AddField(
            model_name='crctrial',
            name='prior_io_ok',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='crctrial',
            name='resources',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.URLField(), blank=True, default='{}', size=None),
        ),
        migrations.AlterField(
            model_name='crctrial',
            name='brief_title',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='crctrial',
            name='comments',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='crctrial',
            name='contact_emails',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.EmailField(max_length=254), blank=True, size=None),
        ),
        migrations.AlterField(
            model_name='crctrial',
            name='contact_phones',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=15), blank=True, size=None),
        ),
        migrations.AlterField(
            model_name='crctrial',
            name='exclusion_criteria',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='crctrial',
            name='gender',
            field=models.CharField(blank=True, choices=[(b'M', b'Male'), (b'F', b'Female')], max_length=1),
        ),
        migrations.AlterField(
            model_name='crctrial',
            name='inclusion_criteria',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='crctrial',
            name='is_crc_trial',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='crctrial',
            name='is_immunotherapy_trial',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='crctrial',
            name='max_age',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='crctrial',
            name='min_age',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='crctrial',
            name='phase',
            field=models.CharField(blank=True, choices=[(b'Phase 1', b'Phase 1'), (b'Early Phase 1', b'Early Phase 1'), (b'Phase 4', b'Phase 4'), (b'Phase 1/Phase 2', b'Phase 1/Phase 2'), (b'Phase 2/Phase 3', b'Phase 2/Phase 3'), (b'Phase 2', b'Phase 2'), (b'Phase 3', b'Phase 3')], max_length=20),
        ),
        migrations.AlterField(
            model_name='crctrial',
            name='program_status',
            field=models.CharField(choices=[(b'Temporarily not available', b'Temporarily not available'), (b'Active, not recruiting', b'Active, not recruiting'), (b'Suspended', b'Suspended'), (b'Recruiting', b'Recruiting'), (b'Withheld', b'Withheld'), (b'Enrolling by invitation', b'Enrolling by invitation'), (b'Completed', b'Completed'), (b'No longer available', b'No longer available'), (b'Unknown status', b'Unknown status'), (b'Withdrawn', b'Withdrawn'), (b'Available', b'Available'), (b'Approved for marketing', b'Approved for marketing'), (b'Not yet recruiting', b'Not yet recruiting'), (b'Terminated', b'Terminated')], max_length=30),
        ),
        migrations.AlterField(
            model_name='crctrial',
            name='urls',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.URLField(max_length=300), blank=True, size=None),
        ),
    ]
