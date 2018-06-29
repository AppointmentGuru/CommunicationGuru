"""
Send push notifications via OneSignal

Required fields:

- channel (will evaluate to tag: channel = ..)
- short_message
"""
import requests, json, os
from django.conf import settings

def get_filter(field, key, relation, value):
    return {
        "field": field,
        "key": key,
        "relation": relation,
        "value": value
    }

class OneSignalBackend:

    def __init__(self, communication):
        self.backend_id = 'services.backends.onesignal.OneSignalBackend'

        self.app_id = os.environ.get('ONESIGNAL_APP_ID')
        token = os.environ.get('ONESIGNAL_APP_TOKEN')
        self.headers = {
            "Content-Type": "application/json; charset=utf-8",
            "Authorization": "Basic {}".format(token)
        }
        self.base_url = 'https://onesignal.com/api/v1'
        self.communication = communication

    def is_valid(self):
        required_fields = ['channel', 'short_message']
        return True

    def __save_result(self, result):
        self.communication.backend_used = self.backend_id
        if result.ok:
            self.communication.backend_message_id = result.json().get('id')
            self.communication.backend_result = result.json()
        else:
            self.communication.backend_id = None
            error_message = {"error": result.content}
            self.communication.backend_result = error_message
        self.communication.save()

    def send(self):

        payload = {
            "app_id": self.app_id,
            "contents": {
                "en": self.communication.short_message
            },
            "filters": [
                get_filter("tag", "practitioner.1", "=", "general")
                # get_filter("tag", "channel", "=", self.communication.channel)
            ]
        }
        url = "{}/notifications".format(self.base_url)
        result = requests.post(url, json=payload, headers=self.headers)
        self.__save_result(result)
        return result

    def receive_reply(self, data):
        '''
        Investigate the incoming data and if you recognize it, then handle the reply
        '''
        pass

    def receive_status(self, data):
        """
        Handle a delivery status report
        """

    def fetch(self, id):
        url = "{}/notifications/{}?app_id={}".format(self.base_url, id, self.app_id)
        return requests.get(url, headers=self.headers).json()

    def search(params):
        pass

