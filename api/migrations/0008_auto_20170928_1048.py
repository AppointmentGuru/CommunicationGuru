# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-28 10:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_auto_20170928_0835'),
    ]

    operations = [
        migrations.AlterField(
            model_name='communicationstatus',
            name='communication',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.Communication'),
        ),
        migrations.AlterField(
            model_name='communicationstatus',
            name='status',
            field=models.CharField(blank=True, db_index=True, default='queued', max_length=255, null=True),
        ),
    ]
