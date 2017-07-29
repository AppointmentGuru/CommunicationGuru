# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-07-13 11:55
from __future__ import unicode_literals

import datetime
from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Communication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sender_email', models.EmailField(blank=True, max_length=254, null=True)),
                ('recipient_channel', models.CharField(blank=True, max_length=255, null=True)),
                ('recipient_id', models.CharField(blank=True, max_length=255, null=True)),
                ('recipient_email', models.EmailField(blank=True, max_length=254, null=True)),
                ('recipient_phone_number', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True)),
                ('subject', models.CharField(blank=True, max_length=255, null=True)),
                ('short_message', models.CharField(blank=True, max_length=144, null=True)),
                ('message', models.TextField(blank=True, null=True)),
                ('context', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('send_date', models.DateTimeField(default=datetime.datetime.now)),
                ('last_sent_date', models.DateTimeField(blank=True, null=True)),
                ('status', models.CharField(choices=[('N', 'New'), ('S', 'Sent'), ('D', 'Delivered'), ('F', 'Failed')], default='N', max_length=10)),
                ('created_date', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('modified_date', models.DateTimeField(auto_now=True, db_index=True)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CommunicationTemplate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('template', models.TextField()),
                ('template_base', models.CharField(max_length=255)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='communication',
            name='template',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.CommunicationTemplate'),
        ),
    ]