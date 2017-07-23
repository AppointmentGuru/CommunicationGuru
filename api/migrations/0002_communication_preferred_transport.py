# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-07-13 12:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='communication',
            name='preferred_transport',
            field=models.CharField(choices=[('email', 'Email'), ('sms', 'SMS')], default='email', max_length=10),
        ),
    ]
