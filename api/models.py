# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.postgres.fields import JSONField, ArrayField
from datetime import datetime
from rest_framework import renderers

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

    def __str__(self):
        return "{}: #{}".format(self.preferred_transport, self.backend_message_id)

    owner = models.CharField(max_length=100, blank=True, null=True)
    object_ids = ArrayField(models.CharField(max_length=100), default=[], blank=True, null=True)

    # the object to which this lineitem is attached
    sender_email = models.EmailField(blank=True, null=True)

    preferred_transport = models.CharField(max_length=10, default='email', choices=TRANSPORTS)

    recipient_channel = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    recipient_id = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    recipient_emails = ArrayField(models.EmailField(), blank=True, null=True, db_index=True)
    recipient_phone_number = PhoneNumberField(blank=True, null=True, db_index=True)
    template = models.ForeignKey(CommunicationTemplate, blank=True, null=True, default=None)

    subject = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    short_message = models.CharField(max_length=144, blank=True, null=True, help_text='Used for short messages')
    message = models.TextField(blank=True, null=True, help_text='Used for emails')

    attached_urls = ArrayField(models.URLField(), default=[], blank=True, null=True, help_text='Urls will be converted to pdf and attached')

    context = JSONField(blank=True, null=True)

    send_date = models.DateTimeField(default=timezone.now, db_index=True)
    last_sent_date = models.DateTimeField(blank=True, null=True, db_index=True)
    status = models.CharField(max_length=10, default='N', choices=SEND_STATUSES, db_index=True)

    created_date = models.DateTimeField(auto_now_add=True, db_index=True)
    modified_date = models.DateTimeField(auto_now=True, db_index=True)

    backend_used = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    backend_message_id = models.CharField(max_length=100, blank=True, null=True, db_index=True)
    backend_result = JSONField(default={}, blank=True, null=True, db_index=True)

    @property
    def as_json_string(self):
        from .serializers import CommunicationDetailSerializer
        serialized = CommunicationDetailSerializer(self)
        return renderers.JSONRenderer().render(serialized.data).decode('utf-8')

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

    def send(self):

        # TODO: only send if send_date is now / in the past

        if self.preferred_transport == 'sms':
            sms = SMS()
            result = sms.send(
                self.short_message,
                self.recipient_phone_number.as_e164)
            return sms.save(self, result)

        if self.preferred_transport == 'email':
            from .tasks import send_email
            return send_email.delay(self.as_json_string)


    def send_html_email(self, subject, plaintext, html):
        return mail.send_mail(subject, plaintext, self.frm, self.to, html_message=html)

    def status_update(self, payload):

        # normalize:
        if isinstance(payload, six.string_types):
            payload = json.loads(payload)

        from api.models import CommunicationStatus, Communication
        from api.models import CommunicationStatus
        status = CommunicationStatus()

        message_id = payload.get('Message-Id')
        if message_id is not None:
            try:
                comm = Communication.objects.get(backend_message_id=message_id)
                status.communication = comm
            except Communication.DoesNotExist:
                pass
        status.status = payload.get('event')
        status.save()

        status.raw_result = payload
        status.save()
        return status


class CommunicationStatus(models.Model):

    communication = models.ForeignKey(Communication, blank=True, null=True, default=None, related_name='communicationstatus')
    status = models.CharField(max_length=255, blank=True, null=True, default='queued', db_index=True)

    raw_result = JSONField(blank=True, null=True)

    created_date = models.DateTimeField(auto_now_add=True, db_index=True)
    modified_date = models.DateTimeField(auto_now=True, db_index=True)


from .signals import *
