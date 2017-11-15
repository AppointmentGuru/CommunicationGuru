# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import renderers
from django.test import TestCase, override_settings
from ..tasks import send_sms, send_email
from ..models import Communication
from ..serializers import CommunicationDetailSerializer
from twilio.rest.resources.messages import Message

@override_settings(CELERY_ALWAYS_EAGER=True)
class SendSMSTestCase(TestCase):

    def setUp(self):
        comm = Communication()
        comm.preferred_transport = 'sms'
        comm.short_message = 'testing'
        comm.recipient_phone_number = '+27832566533'

        serialized = CommunicationDetailSerializer(comm)

        parsed = renderers.JSONRenderer().render(serialized.data).decode("utf-8")
        self.result = send_sms.delay(parsed)

        # communication.backend_result = format_sms_result(result)
        # communication.save()

        self.comm = comm

    def test_is_ok(self):
        assert self.result.status == 'SUCCESS'

    def test_returns_twilio_message(self):
        assert isinstance(self.result.result, Message)

@override_settings(CELERY_ALWAYS_EAGER=True)
class SendEmailTestCase(TestCase):

    def setUp(self):
        comm = Communication()
        comm.preferred_transport = 'sms'
        comm.short_message = 'testing'
        comm.recipient_phone_number = '+27832566533'

@override_settings(CELERY_ALWAYS_EAGER=True)
class SendEmailWithUrlAttachmentTestCase(TestCase):

    def setUp(self):
        comm = Communication()
        comm.preferred_transport = 'sms'
        comm.message = 'testing. testing, 1.2.3'
        comm.subject = 'this is a test'
        comm.recipient_emails = ['tech@appointmentguru.co', 'supoprt@appointmentguru.co']
        comm.sender_email = 'no-reply@appointmentguru.co'

        serialized = CommunicationDetailSerializer(comm)
        parsed = renderers.JSONRenderer().render(serialized.data).decode('utf-8')

        self.result = send_email.delay(parsed)
        self.comm = comm

    def test_is_ok(self):
        assert self.result.status == 'SUCCESS'

