"""
Send push notifications via OneSignal
"""
import requests, json

class OneSignalBackend:

    def __init__(self):
        self.app_id = os.environ.get('ONESIGNAL_APP_ID')
        token = os.environ.get('ONESIGNAL_APP_TOKEN')
        self.header = {
            "Content-Type": "application/json; charset=utf-8",
            "Authorization": "Basic {}".format(token)
        }
        self.base_url = 'https://onesignal.com/api/v1'


    def send(self, message, to, **kwargs):

        payload = {
            "app_id": self.app_id,
            "included_segments": ["All"],
            "contents": {
                "en": "English Message"
            }
        }
        url = "{}/notifications".format(self.base_url)
        return requests.post(url, payload, )

    def fetch():
        pass

    def search(params):
        pass

