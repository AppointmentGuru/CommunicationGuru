# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from django.contrib.auth import get_user_model
from ..models import Communication

class SMSBackendTestCase(TestCase):

    def setUp(self):

        data = {
            "recipient_phone_number": "+27832566533",
            "short_message": "testing",
            "preferred_transport": "sms",
        }
        self.message = Communication.objects.create(**data)

    def test_it_sends_an_sms(self):
        result = self.message.send()