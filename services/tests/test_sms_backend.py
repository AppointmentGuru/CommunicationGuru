from django.test import TestCase, override_settings
from django.contrib.auth import get_user_model
from phonenumbers import PhoneNumber
from services.sms import SMS
from services.backends.mocksms import MockSMSBackend
import unittest

@override_settings(SANDBOX_MODE=False)
@override_settings(SMS_BACKEND='services.backends.mocksms.MockSMSBackend')
class PhoneAuthFormTestCase(TestCase):

	def setUp(self):
		pass

	@unittest.mock.patch.object(MockSMSBackend, 'send')
	def test_send_normal_text_sms(self, mock_sms):
		message = SMS().send('test', '+27832566533')

		mock_sms.assert_called_once_with('test', '+27832566533')

	@unittest.mock.patch.object(MockSMSBackend, 'send')
	def test_send_PhoneNumber_sms(self, mock_sms):
		message = SMS().send('test', '+27832566533')
		mock_sms.assert_called_once_with('test', '+27832566533')



