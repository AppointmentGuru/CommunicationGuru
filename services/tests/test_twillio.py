from django.test import TestCase
from django.conf import settings
from services.backends.twillio import TwillioBackend
from twilio.rest.resources import Messages
import mock, unittest

# TODO: refactor to backends

class SMSTestCase(TestCase):

	def setUp(self):
		pass

	@mock.patch.object(Messages, 'create_instance')
	def test_send_sms(self, mock_twillio):

		sms = TwillioBackend()
		msg = sms.send("testing testing 123", "+27832566533")
		expected_args = {
			'from': settings.TWILLIO_PHONE_NUMBER, 
			'to': '+27832566533', 
			'body': 'testing testing 123'
		}
		mock_twillio.assert_called_once_with(expected_args)
		