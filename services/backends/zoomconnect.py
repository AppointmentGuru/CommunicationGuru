"""
A backend for sending smses using: https://www.zoomconnect.com
"""

import requests
from django.conf import settings
from api.models import CommunicationStatus

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
            if isinstance(tags, list): tags = (',').join(tags)
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

    def update_status(self, payload):
        message_id = self.get_id_from_payload(payload)
        comm = Communication.objects.get(backend_message_id=message_id)
        status = CommunicationStatus()
        status.communication = comm
        status.raw_result = payload
        status.status = payload['status']
        status.save()

    def get_id_from_payload(self, payload):
        return payload['messageId']

    # def reply_received(self, payload):
    #     CommunicationStatus.objects.create(raw_result=payload)

    def search(self, params={}, **kwargs):
        url, credentials, headers = self._get_url('/v1/messages/all')
        params.update(credentials)
        print(url)
        print(params)
        print(headers)
        return  requests.get(url, params=params, headers=headers)
