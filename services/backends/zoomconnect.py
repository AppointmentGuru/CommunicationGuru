"""
A backend for sending smses using: https://www.zoomconnect.com
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
        return response.content

    def fetch(self, id, **kwargs):
        url, params, headers = self._get_url('/v1/messages/{}'.format(id))
        return requests.get(url, params=params, headers=headers)

    def search(self, params={}, **kwargs):
        url, credentials, headers = self._get_url('/v1/messages/')
        params.update(credentials)
        return requests.get(url, params=params, headers=headers)