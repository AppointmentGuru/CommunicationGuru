from twilio.rest import TwilioRestClient
from django.conf import settings

class TwillioBackend:

	def __init__(self):
        account_sid = settings.TWILLIO_SID # Your Account SID from www.twilio.com/console
        auth_token  = settings.TWILLIO_AUTH_TOKEN  # Your Auth Token from www.twilio.com/console

		self.client = TwilioRestClient(account_sid, auth_token)
		self.from_number = settings.TWILLIO_PHONE_NUMBER
		# todo: backends:

	def send(self, message, to):

		return self.client.messages.create(
            body=message,
            to=to,
            from_=self.from_number)

    def fetch(self, id):
        '''
        Get the data on this message
        '''
        return client.messages.get(id).__dict__

