# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from django.test import TestCase, override_settings
from .datas import MAILGUN_EMAIL, MAILGUN_EMAIL_NO_MESSAGE_ID
from ..email import Email
from api.models import Communication
import json

@override_settings(SMS_BACKEND='services.backends.mocksms.MockSMSBackend')
class SMSSendTestCase(TestCase):

    def setUp(self):
        comm = Communication()
        comm.short_message = 'testing, testing. 1.2.3'
        comm.recipient_phone_number = '+27832566533'
        comm.preferred_transport = 'sms'
        comm.save()

        self.comm = comm

    def test_sends(self):
        assert isinstance(self.comm, Communication)

    # def test_communication_communication_result(self):
    #     '''TODO: this should be an integration test'''
    #     expected_fields = ['raw_result', 'backend_used', 'backend_message_id']
    #     for field in expected_fields:
    #         assert getattr(self.comm, field, None) is not None