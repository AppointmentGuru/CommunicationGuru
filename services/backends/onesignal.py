"""
Send push notifications via OneSignal
"""
import requests, json, os
from django.conf import settings

class OneSignalBackend:

    def __init__(self):
        self.app_id = settings.ONESIGNAL_APP_ID
        self.backend_id = settings.PUSH_BACKEND
        token = settings.ONESIGNAL_APP_TOKEN
        self.header = {
            "Content-Type": "application/json; charset=utf-8",
            "Authorization": "Basic {}".format(token)
        }
        self.base_url = 'https://onesignal.com/api/v1'

    def send(self, communication, **kwargs):
        segments = communication.channel

        # in sandbox mode only ever sent to test channel
        if settings.SANDBOX_MODE:
            segments = ["Test users"]

        payload = {
            "app_id": self.app_id,
            "included_segments": segments,
            "headings": {
                "en": communication.subject
            },
            "contents": {
                "en": communication.short_message
            }
        }
        url = "{}/notifications".format(self.base_url)
        return requests.post(
                url,
                headers=self.header,
                data=json.dumps(payload))

    def fetch(self, id):
        url = '{}/notifications/{}?app_id={}'.format(self.base_url, id, self.app_id)
        return requests.get(url, headers=self.header)

    def search(params):
        pass

