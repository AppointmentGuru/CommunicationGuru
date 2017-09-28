# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from ..lib import CommunicationGuru

from .testutils import assert_response, get_proxy_headers
import random

BASE_URL = 'http://web:8000'

class CommunicationGuruLibTestCase(TestCase):

    def setUp(self):
        self.comms = CommunicationGuru(BASE_URL)

    def test_send_simple_email(self):
        random_string = str(random.random())
        subject = 'test: {}'.format(random_string)
        result = self.comms.send_email(['info@38.co.za'], subject, 'this is a test', from_email='support@appointmentguru.co')
        import ipdb;ipdb.set_trace()

