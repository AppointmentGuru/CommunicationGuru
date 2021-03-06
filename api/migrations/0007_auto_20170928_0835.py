# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-28 08:35
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_communicationstatus_raw_result'),
    ]

    operations = [
        migrations.AddField(
            model_name='communication',
            name='backend_result',
            field=django.contrib.postgres.fields.jsonb.JSONField(default={}),
        ),
        migrations.AddField(
            model_name='communication',
            name='backend_used',
            field=models.CharField(blank=True, db_index=True, max_length=255, null=True),
        ),
    ]
