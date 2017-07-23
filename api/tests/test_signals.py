# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from django.contrib.auth import get_user_model
from ..models import Communication, CommunicationTemplate

class SignalsTestCase(TestCase):

    def setUp(self):
        pass

    def test_apply_template_on_save(self):
        pass

    def test_send_on_post_save(self):
        pass