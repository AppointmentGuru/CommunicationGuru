from django.test import TestCase

from ..helpers import msg

class HelpersTestCase(TestCase):

    def test_minimal_send_sms_msg(self):
        msg('testing', '+27832566533')