# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-07-13 14:08
from __future__ import unicode_literals

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20170713_1216'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='communication',
            name='recipient_email',
        ),
        migrations.AddField(
            model_name='communication',
            name='recipient_emails',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.EmailField(max_length=254), blank=True, null=True, size=None),
        ),
    ]
