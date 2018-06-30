# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core import mail
from django.test import TestCase
from django.contrib.auth import get_user_model
from ..models import Communication
import unittest

class EmailBackendTestCase(TestCase):

    def setUp(self):

        self.user = get_user_model().objects.create_user(username='joe')
        data = {
            "subject": "testing",
            "message": "this is the body of the email",
            "recipient_emails": ["jane@soap.com", "jill@soap.com"],
            "sender_email": "joe@soap.com",
            "preferred_transport": "email"
        }
        self.message = Communication.objects.create(**data)

    @unittest.skip("will circle back to this later")
    def test_it_sends_an_email(self):

        assert len(mail.outbox) == 1, \
            'Expected 1 message to be in outbox. There where: {}'.format(len(mail.outbox))

    def test_it_sends_to_correct_recipients(self):
        pass

    def test_it_sets_correct_subject(self):
        pass

    def test_it_sets_correct_message(self):
        pass