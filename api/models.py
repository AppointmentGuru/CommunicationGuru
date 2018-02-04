# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.db.models import Q
from django.utils.module_loading import import_string

from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.postgres.fields import JSONField, ArrayField
from rest_framework import renderers

from services.sms import SMS
from services.email import Email
import mistune, six

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

    def __str__(self):
        return self.subject

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    subject = models.CharField(max_length=255, blank=True, null=True)
    short_message = models.CharField(max_length=144, blank=True, null=True)
    message = models.TextField(blank=True, null=True)

    template_base = models.CharField(max_length=255)


class Communication(models.Model):

    def __str__(self):
        return "{}: #{}".format(self.preferred_transport, self.backend_message_id)

    related_communication = models.ForeignKey('Communication', blank=True, null=True)

    owner = models.CharField(max_length=100, blank=True, null=True)
    # appointment:123 client:345 user:
    # communicatoin/appointment/:id
    # tags = ArrayField
    object_ids = ArrayField(models.CharField(max_length=255), default=[], blank=True, null=True)
    tags = ArrayField(models.CharField(max_length=255), default=[], blank=True, null=True)
    channel = ArrayField(models.CharField(max_length=255), default=[], blank=True, null=True)

    # the object to which this lineitem is attached
    sender_email = models.EmailField(blank=True, null=True)
    sender_phone_number = PhoneNumberField(blank=True, null=True, db_index=True)
    preferred_transport = models.CharField(max_length=10, default='email', choices=TRANSPORTS)

    recipient_id = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    recipient_emails = ArrayField(models.EmailField(blank=True, null=True), blank=True, null=True, db_index=True)
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

    cancel_signal = models.BooleanField(default=False)

    @classmethod
    def sms(cls, owner, from_number, to_number, message, tags=[], object_ids=[]):
        '''
        Creates a short message
        '''
        cls.owner = owner
        cls.sender_phone_number = from_number
        cls.recipient_phone_number = to_number
        cls.short_message = message
        cls.tags = tags
        cls.object_ids = object_ids
        cls.preferred_transport = 'sms'
        cls.save()

    @classmethod
    def get_from_payload(cls, backend, transport, payload):
        message_id = None
        if transport == 'sms':
            message_id = SMS(settings.BACKENDS[backend])\
                            .get_id_from_payload(payload)
        if transport == 'email':
            message_id = (Email(settings.BACKENDS[backend])
                          .get_id_from_payload(payload))

        try:
            # normalize_message_id:
            try:
                int(message_id)
                return cls.objects.get(id=message_id)
            except:
                return cls.objects.get(backend_message_id=message_id)
        except Communication.DoesNotExist:
            return None

    @property
    def status_list(self):
        statuses = self.communicationstatus.all().order_by('created_date')
        return [status.status for status in statuses]

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
                # apply markdown:
                if field != 'subject':
                    rendered = mistune.markdown(rendered)
                setattr(self, field, rendered)
            if with_save:
                self.save()
            return self

    def get_backend(self):
        '''
        Returns the backend object associated with this message, None if no backend found
        '''
        if self.preferred_transport == 'email':
            return import_string('services.email.Email')(
                to=self.recipient_emails,
                frm=self.sender_email)

        if self.backend_used is not None:
            return import_string(self.backend_used)()

        return None

    def send(self, tags=[]):

        # TODO: only send if send_date is now / in the past

        if self.preferred_transport == 'sms':
            sms = SMS()
            tags.append('msg:{}'.format(self.id))
            extra_data = {'tags': tags}
            message_id, result = sms.send(
                self.short_message,
                self.recipient_phone_number.as_e164,
                **extra_data)

            self.backend_used = settings.SMS_BACKEND
            self.backend_message_id = message_id
            self.backend_result = result
            self.save()

            return result
            # return sms.save(self, result)

        if self.preferred_transport == 'email':
            from .tasks import send_email
            return send_email.delay(self.as_json_string)

    def update_status(self, payload, **kwargs):

        # normalize:
        if isinstance(payload, six.string_types):
            payload = json.loads(payload)

        backend = self.get_backend()
        return backend.update_status(self, payload)


    def reply_received(self, payload, **kwargs):
        if isinstance(payload, six.string_types):
            payload = json.loads(payload)

        backend = self.get_backend()
        backend.reply_received(self, payload)


    def send_html_email(self, subject, plaintext, html):
        return mail.send_mail(subject, plaintext, self.frm, self.to, html_message=html)



class CommunicationStatus(models.Model):

    communication = models.ForeignKey(Communication, blank=True, null=True, default=None, related_name='communicationstatus')
    status = models.CharField(max_length=255, blank=True, null=True, default='queued', db_index=True)

    raw_result = JSONField(blank=True, null=True)

    created_date = models.DateTimeField(auto_now_add=True, db_index=True)
    modified_date = models.DateTimeField(auto_now=True, db_index=True)


from .signals import *
