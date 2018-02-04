"""
A backend for sending smses using: https://www.zoomconnect.com
"""

import requests
from django.conf import settings
from api.models import CommunicationStatus, Communication


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

        id = response.json().get('messageId')
        data = response.json()
        return (id, data)

    def fetch(self, id, **kwargs):
        url, params, headers = self._get_url('/v1/messages/{}'.format(id))
        return requests.get(url, params=params, headers=headers)

    def update_status(self, communication, payload, **kwargs):
        status = CommunicationStatus()
        status.communication = communication
        status.raw_result = payload
        status.status = payload['status']
        status.save()

    def reply_received(self, original_communication, payload, *args, **kwargs):
        comm = Communication()
        comm.related_communication = original_communication
        comm.short_message = payload.get('message')
        comm.recipient_phone_number = payload.get('from')
        comm.sender_phone_number = original_communication.sender_phone_number
        comm.save()

    def search(self, params={}, **kwargs):
        url, credentials, headers = self._get_url('/v1/messages/all')
        params.update(credentials)
        print(url)
        print(params)
        print(headers)
        return requests.get(url, params=params, headers=headers)

    @staticmethod
    def get_id_from_payload(payload):
        is_status_message = 'status' in payload
        if not is_status_message: # it's a reply:
            tags = payload.get('dataField', None)
            if tags is not None:
                comm_id = [tag.split(':')[1] \
                            for tag in tags.split(',')\
                            if 'msg' in tag][0]
                return comm_id
        return payload.get('messageId', None)
