# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-10-31 19:06
from __future__ import unicode_literals

import django.contrib.postgres.fields
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_auto_20170928_1048'),
    ]

    operations = [
        migrations.AddField(
            model_name='communication',
            name='attached_urls',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.URLField(), blank=True, default=[], help_text='Urls will be converted to pdf and attached', null=True, size=None),
        ),
        migrations.AlterField(
            model_name='communication',
            name='backend_result',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, db_index=True, default={}, null=True),
        ),
        migrations.AlterField(
            model_name='communication',
            name='message',
            field=models.TextField(blank=True, help_text='Used for emails', null=True),
        ),
        migrations.AlterField(
            model_name='communication',
            name='short_message',
            field=models.CharField(blank=True, help_text='Used for short messages', max_length=144, null=True),
        ),
        migrations.AlterField(
            model_name='communicationstatus',
            name='communication',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='communicationstatus', to='api.Communication'),
        ),
    ]
