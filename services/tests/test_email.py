# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from .datas import MAILGUN_EMAIL, MAILGUN_EMAIL_NO_MESSAGE_ID
from ..email import Email
from api.models import Communication
import json

class EmailTestCase(TestCase):

    def setUp(self):
        comm = Communication()
        comm.subject = 'testing'
        comm.message = 'foo'
        comm.recipient_emails = ['joe@soap.com']
        comm.sender_email = 'jane@soap.com'
        comm.save()

        comm.backend_message_id = '<20170928084650.52111.137F1AF584D57071@appointmentguru.co>'
        comm.save()

        self.comm = comm

        self.eml = Email(None)
        self.status = self.eml.status_update(MAILGUN_EMAIL)

    def test_sets_communication(self):
        assert self.status.communication_id == self.comm.id, \
            'Expected communication_id to be: {}. Got: {}' \
                .format(self.comm.id, self.status.communication_id)

    def test_sets_status(self):
        assert self.status.status == 'delivered'

    def test_sets_payload(self):
        assert self.status.raw_result is not None

    def test_handles_payload_as_string(self):
        status = self.eml.status_update(json.dumps(MAILGUN_EMAIL))
        assert status.raw_result is not None

    def test_it_handles_if_no_communication_is_found(self):
        status = self.eml.status_update(MAILGUN_EMAIL_NO_MESSAGE_ID)

        assert status.communication is None
