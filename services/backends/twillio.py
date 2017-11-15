from twilio.rest import TwilioRestClient
from django.conf import settings
import six, json

class TwillioBackend:

    def __init__(self):
        account_sid = settings.TWILLIO_SID # Your Account SID from www.twilio.com/console
        auth_token  = settings.TWILLIO_AUTH_TOKEN  # Your Auth Token from www.twilio.com/console

        self.client = TwilioRestClient(account_sid, auth_token)
        self.from_number = settings.TWILLIO_PHONE_NUMBER
        # todo: backends:

    def send(self, message, to_number):

        if not to_number.startswith('+'):
            to_number = '+{}'.format(to_number)

        return self.client.messages.create(
            body=message,
            to=to_number,
            from_=self.from_number,
            StatusCallback=settings.TWILLIO_STATUS_CALLBACK)

    def as_json(self):
        fields = [
            'name', 'base_uri', 'sid',
            # 'date_created', 'date_updated', 'date_send',
            'account_sid', 'to', 'messaging_service_sid',
            'body', 'status', 'num_segments', 'num_media', 'direction',
            'api_version', 'price', 'price_unit', 'error_code', 'error_message',
            'from_',
        ]
        json_result = {}
        for field in fields:
            value = getattr(result, field, None)
            json_result[field] = value
        return json_result

    def fetch(self, id):
        '''
        Get the data on this message
        '''
        return client.messages.get(id).__dict__

    def save(self, communication, result):
        from api.models import CommunicationStatus
        status = CommunicationStatus()
        status.status = result.status
        status.communication = communication

        communication.backend_used = settings.SMS_BACKEND
        communication.backend_message_id = result.sid
        communication.save()

        #save raw response:
        parsed_data = self.as_json()
        communication.raw_result = parsed_data
        communication.save()

    def status_update(self, payload):
        ''' TODO: standardize this'''

        # normalize:
        if isinstance(payload, six.string_types):
            payload = json.loads(payload)

        from api.models import CommunicationStatus, Communication
        from api.models import CommunicationStatus
        status = CommunicationStatus()

        message_id = payload.get('SmsSid', None)
        if message_id is not None:
            try:
                comm = Communication.objects.get(backend_message_id=message_id)
                status.communication = comm
            except Communication.DoesNotExist:
                pass
        status.status = payload.get('MessageStatus')
        status.save()

        status.raw_result = payload
        status.save()
        return status

