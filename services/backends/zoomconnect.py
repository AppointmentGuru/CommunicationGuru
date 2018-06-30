"""
A backend for sending smses using: https://www.zoomconnect.com
"""

import requests
from django.conf import settings
from api.models import Communication, CommunicationStatus
from api.helpers import create_short_message

class ZoomSMSBackend:

    def __init__(self, communication):
        self.backend_id = 'services.backends.zoomconnect.ZoomSMSBackend'
        self.communication = communication

        # map zoom statuses to standard statuses
        self.status_map = {
            'DELIVERED': 'D',
            'SENT': 'S',
            'SCHEDULED': 'N',
            'FAILED': 'F',
            'FAILED_REFUNDED': 'F',
            'FAILED_OPTOUT': 'F',
        }

    @classmethod
    def from_payload(cls, backend, data):
        id = data.get('messageId')
        communication = Communication.objects.get(
                            backend_used=backend,
                            backend_message_id=id
                        )
        return cls(communication)


    def _get_url(self, path):
        url = '{}/app/api/rest{}'.format(settings.ZOOM_BASE_URL, path)
        params = {
            "email": settings.ZOOM_EMAIL,
            "token": settings.ZOOM_API_TOKEN
        }
        headers = {
            'Content-type': 'application/json',
            'Accept': 'application/json'
        }
        return (url, params, headers)

    def __save_result(self, result):
        self.communication.backend_used = self.backend_id
        if result.ok:
            self.communication.backend_message_id = result.json().get('messageId')
            self.communication.backend_result = result.json()
        else:
            self.communication.backend_message_id = None
            error_message = {"error": result.content}
            self.communication.backend_result = error_message
        self.communication.save()

    def send(self):
        url, params, headers = self._get_url('/v1/sms/send')

        data = {
            "recipientNumber": self.communication.recipient_phone_number.as_e164,
            "message": self.communication.short_message,
        }
        # "app:310,pra:684,cli:685,pro:12345"
        tags = (",").join(self.communication.tags)
        campaign = "{};".format(self.communication.channel)
        if tags is not None:
            data["dataField"] = tags[0:50]
        if campaign is not None:
            data['campaign'] = campaign

        response = requests.post(url, json=data, params=params, headers=headers)
        self.__save_result(response)
        return response

    def fetch(self, id, **kwargs):
        url, params, headers = self._get_url('/v1/messages/{}'.format(id))
        return requests.get(url, params=params, headers=headers)

    def handle_reply(self, data):
        '''
        Investigate the incoming data and if you recognize it, then handle the reply
        '''
        expected_fields = ['messageId', 'message', 'nonce', 'nonce-date']
        for field in expected_fields:
            if data.get(field) is None: return False

        message_id = data.get('messageId')
        message = data.get('message')

        channel = self.communication.channel

        reply = create_short_message(channel, message)
        reply.reply_to = self.communication
        reply.save()
        return reply

    def receive_status(self, data):
        """
        Handle a delivery status report
        """
        received_status = data.get('status')
        status = CommunicationStatus()
        status.communication = self
        status.raw_result = data
        status.status = getattr(self.status_map, received_status, 'UK')
        status.save()
        return status

    def search(self, params={}, **kwargs):
        url, credentials, headers = self._get_url('/v1/messages/all')
        params.update(credentials)
        return  requests.get(url, params=params, headers=headers)