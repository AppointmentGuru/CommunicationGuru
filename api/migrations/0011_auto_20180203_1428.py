# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-02-03 14:28
from __future__ import unicode_literals

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_auto_20180122_1733'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='communication',
            name='recipient_channel',
        ),
        migrations.AddField(
            model_name='communication',
            name='channel',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=255), blank=True, default=[], null=True, size=None),
        ),
        migrations.AddField(
            model_name='communication',
            name='related_communication',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.Communication'),
        ),
        migrations.AddField(
            model_name='communication',
            name='sender_phone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, db_index=True, max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='communication',
            name='tags',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=255), blank=True, default=[], null=True, size=None),
        ),
        migrations.AlterField(
            model_name='communication',
            name='object_ids',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=255), blank=True, default=[], null=True, size=None),
        ),
    ]
