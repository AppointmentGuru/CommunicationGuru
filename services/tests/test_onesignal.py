# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from services.backends.onesignal import OneSignalBackend
from api.models import Communication
import unittest

class OneSignalBackendTestCase(TestCase):

    def setUp(self):

        self.be = OneSignalBackend()

    @unittest.skip("Integration test")
    def test_send_notification(self):

        res = self.be.send(None, None)
        assert res.status == 200


    def test_get_notification(self):

        res = self.be.fetch('9647b56e-0d6a-4dab-9556-b1d9652fc0b9')
        import ipdb;ipdb.set_trace()