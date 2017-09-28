# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from .datas import MAILGUN_EMAIL
from ..email import Email
from api.models import Communication

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

        eml = Email(None)
        self.status = eml.status_update(MAILGUN_EMAIL)

    def test_sets_communication(self):

        assert self.status.communication_id == self.comm.id

    def test_sets_status(self):
        assert self.status.status == 'delivered'

    def test_sets_payload(self):
        assert self.status.raw_result is not None
