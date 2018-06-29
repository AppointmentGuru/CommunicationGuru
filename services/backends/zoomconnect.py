"""
A backend for sending smses using: https://www.zoomconnect.com

Reply data:

{
  "date": "201806292136",
  "dataField": "cli:1,app:21502,pra:3001,pro:17554,",
  "repliedToMessageId": "5b361e32e396c8e42e098807",
  "messageId": "5b368a2be396c8e42e0ac61f",
  "campaign": "practitioner-3001",
  "from": "+27832566533",
  "to": "27987654349",
  "nonce-date": "20180629214112",
  "message": "Testing testing 123",
  "nonce": "5cfb2a28-c660-4b4d-aa6e-aeafc8f04563",
  "checksum": "072a46e882faab427434cb8f2e4e01159cf6f9ab"
}
"""

import requests
from django.conf import settings

class ZoomSMSBackend:

    def __init__(self):
        pass

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

    def send(self, message, to, **kwargs):
        url, params, headers = self._get_url('/v1/sms/send')

        data = {
            "recipientNumber": to,
            "message": message
        }
        tags = kwargs.get('tags', None)
        campaign = kwargs.get('campaign', None)
        if tags is not None:
            data["dataField"] = tags[0:50]
        if campaign is not None:
            data['campaign'] = campaign

        response = requests.post(url, json=data, params=params, headers=headers)
        if response.status_code > 201:
            raise Exception(response.content)
        return response.content

    def fetch(self, id, **kwargs):
        url, params, headers = self._get_url('/v1/messages/{}'.format(id))
        return requests.get(url, params=params, headers=headers)

    def receive_reply(self, data):
        '''
        Investigate the incoming data and if you recognize it, then handle the reply
        '''
        pass

    def receive_status(self, data):
        """
        Handle a delivery status report
        """
        pass

    def search(self, params={}, **kwargs):
        url, credentials, headers = self._get_url('/v1/messages/all')
        params.update(credentials)
        print(url)
        print(params)
        print(headers)
        return  requests.get(url, params=params, headers=headers)