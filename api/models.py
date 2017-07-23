# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.postgres.fields import JSONField, ArrayField
from datetime import datetime

from services.sms import SMS
from services.email import Email

from django.template import Context
from django.template import Template

SEND_STATUSES = [
    ('N', 'New'),
    ('S', 'Sent'),
    ('D', 'Delivered'),
    ('F', 'Failed'),
]

TRANSPORTS = [
    ('email', 'Email'),
    ('sms', 'SMS'),
    # ('im', 'IM (e.g.: Slack, Hipchat)'),
    # ('notification', 'Push Notification'),
]

class CommunicationTemplate(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    subject = models.CharField(max_length=255, blank=True, null=True)
    short_message = models.CharField(max_length=144, blank=True, null=True)
    message = models.TextField(blank=True, null=True)

    template_base = models.CharField(max_length=255)

class Communication(models.Model):

    # the object to which this lineitem is attached
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    sender_email = models.EmailField(blank=True, null=True)

    preferred_transport = models.CharField(max_length=10, default='email', choices=TRANSPORTS)

    recipient_channel = models.CharField(max_length=255, blank=True, null=True)
    recipient_id = models.CharField(max_length=255, blank=True, null=True)
    # make this an arrayfield?
    recipient_emails = ArrayField(models.EmailField(), blank=True, null=True)
    recipient_phone_number = PhoneNumberField(blank=True, null=True)
    template = models.ForeignKey(CommunicationTemplate, blank=True, null=True, default=None)

    subject = models.CharField(max_length=255, blank=True, null=True)
    short_message = models.CharField(max_length=144, blank=True, null=True)
    message = models.TextField(blank=True, null=True)

    context = JSONField(blank=True, null=True)

    send_date = models.DateTimeField(default=datetime.now)
    last_sent_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=10, default='N', choices=SEND_STATUSES)

    created_date = models.DateTimeField(auto_now_add=True, db_index=True)
    modified_date = models.DateTimeField(auto_now=True, db_index=True)

    def apply_template(self, with_save=True):
        '''given a CommunicationTemplate and context: generate subject, short_message and message'''

        if self.template is not None:
            fields = ['subject', 'short_message', 'message']
            for field in fields:
                message = getattr(self.template, field, '')
                template = Template(message)
                context = Context(self.context)
                rendered = template.render(context)
                setattr(self, field, rendered)
            if with_save:
                self.save()
            return self

    def send(self, force=False):

        if self.preferred_transport == 'sms':
            result = SMS().send(self.short_message, self.recipient_phone_number)
            return result
        if self.preferred_transport == 'email':
            emailer = Email(self.recipient_emails, self.sender_email)
            result = emailer.send(
                        self.subject,
                        self.message,
                        self.message
                    )
            return result

from .signals import *
