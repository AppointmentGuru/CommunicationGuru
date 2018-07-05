# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.postgres.fields import JSONField, ArrayField
from rest_framework import renderers

from services.sms import SMS
import mistune, importlib, jsonschema

from django.template import Context
from django.template import Template

SEND_STATUSES = [
    ('N', 'New'),
    ('Q', 'Queued'),
    ('S', 'Sent'),
    ('D', 'Delivered'),
    ('O', 'Opened'),
    ('C', 'Clicked'),
    ('UK', 'Unknown'),
    ('F', 'Failed'),
]

TRANSPORTS = [
    ('email', 'Email'),
    ('sms', 'SMS'),
    # ('im', 'IM (e.g.: Slack, Hipchat)'),
    ('notification', 'Push Notification'),
]


class CommunicationTemplate(models.Model):

    def __str__(self):
        return self.subject

    owner = models.CharField(max_length=42, blank=True, null=True)
    slug = models.SlugField(blank=True, null=True, help_text='A friendly lookup for this template')

    # meta infos:
    name = models.CharField(max_length=255, blank=True, null=True, help_text='A friendly name describing what this template is for')
    description = models.TextField(blank=True, null=True, help_text='A longer description of the purpose of this communication')

    subject = models.CharField(max_length=255, blank=True, null=True)
    short_message = models.TextField(blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    schema = JSONField(blank=True, null=True, help_text='Build schemas at: https://jsonschema.net')

    template_base = models.CharField(max_length=255, blank=True, null=True)

    # class Meta:
    #     unique_together = ('owner', 'slug',)


class Communication(models.Model):

    def __str__(self):
        return "{}: #{}".format(self.preferred_transport, self.backend_message_id)

    reply_to = models.ForeignKey('Communication', blank=True, null=True)
    # isOwner
    owner = models.CharField(max_length=100, blank=True, null=True)
    # appointment:123 client:345 user:
    # communicatoin/appointment/:id
    # tags = ArrayField
    object_ids = ArrayField(models.CharField(max_length=100), default=[], blank=True, null=True)

    # the object to which this lineitem is attached
    sender_email = models.EmailField(blank=True, null=True)

    channel = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    backends = ArrayField(
                models.CharField(max_length=255, blank=True, null=True),
                default=[],
                blank=True,
                null=True,
                help_text='An array of backends to try use to send. Will try in order until one is successful'
               )

    tags = ArrayField(
                models.CharField(max_length=255, blank=True, null=True),
                default=[],
                blank=True,
                null=True
               )

    recipient_id = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    recipient_emails = ArrayField(models.EmailField(blank=True, null=True), blank=True, null=True, db_index=True)
    recipient_phone_number = PhoneNumberField(blank=True, null=True, db_index=True)
    template = models.ForeignKey(CommunicationTemplate, blank=True, null=True, default=None)

    subject = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    short_message = models.TextField(blank=True, null=True, help_text='Used for short messages')
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

    # legacy fields:
    preferred_transport = models.CharField(max_length=10, default='email', choices=TRANSPORTS)
    recipient_channel = models.CharField(max_length=255, blank=True, null=True, db_index=True)

    def get_by_backend(backend, backend_message_id):
        return Communication.objects.get(
            backend_used = backend,
            backend_message_id = backend_message_id
        )

    @property
    def status_list(self):
        statuses = self.communicationstatus.all().order_by('created_date')
        return [status.status for status in statuses]

    @property
    def as_json_string(self):
        from .serializers import CommunicationDetailSerializer
        serialized = CommunicationDetailSerializer(self)
        return renderers.JSONRenderer().render(serialized.data).decode('utf-8')

    def validate_template_context(self):
        if self.template is not None and self.template:
            try:
                jsonschema.validate(self.context, self.template.schema)
            except jsonschema.exceptions.ValidationError as err:
                return (False, err.message)

        return (True, None)


    def apply_template(self, with_save=True):
        '''given a CommunicationTemplate and context: generate subject, short_message and message'''

        if self.template is not None:
            fields = ['subject', 'short_message', 'message']
            for field in fields:
                message = getattr(self.template, field, '')
                template = Template(message)
                context = Context(self.context)
                rendered = template.render(context)
                # apply markdown (only to long message)
                if field == 'message':
                    rendered = mistune.markdown(rendered)
                setattr(self, field, rendered)
            if with_save:
                self.save()
            return self

    def __get_backend(self):
        from .helpers import get_backend
        return get_backend(self.backend_used, self)

    def get_remote(self):

        return self.__get_backend().fetch(self.backend_message_id)

    def handle_reply(self, data):
        """
        Route to the backend's handle_reply function
        which should send the message on to the default
        backend for handling either short messages or
        long messages(emails)
        """
        self.__get_backend().handle_reply(data)

    def send(self):
        from .helpers import get_backend
        for backend in self.backends:
            return get_backend(backend, self).send()

        # TODO: only send if send_date is now / in the past

        # if self.preferred_transport == 'sms':
        #     sms = SMS()
        #     result = sms.send(
        #         self.short_message,
        #         self.recipient_phone_number.as_e164)
        #     return result
        #     # return sms.save(self, result)

        # if self.preferred_transport == 'email':
        #     from .tasks import send_email
        #     return send_email.delay(self.as_json_string)

    def send_html_email(self, subject, plaintext, html):
        return mail.send_mail(subject, plaintext, self.frm, self.to, html_message=html)

    def status_update(self, payload):

        # normalize:
        if isinstance(payload, six.string_types):
            payload = json.loads(payload)

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
    status = models.CharField(max_length=255, choices=SEND_STATUSES, blank=True, null=True, default='N', db_index=True)

    raw_result = JSONField(blank=True, null=True)

    created_date = models.DateTimeField(auto_now_add=True, db_index=True)
    modified_date = models.DateTimeField(auto_now=True, db_index=True)


from .signals import *
