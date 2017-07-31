from django.test import TestCase
import json

class WebHookTestCase(TestCase):

    def test_slack_webhook_payload(self):

        data = {
            "foo": "bar",
            "baz": "bus"
        }
        result = self.client.post('/incoming/slack/', json.dumps(data), content_type='application/json')


{
    "name": "message.json",
    "title": "message",
    "mimetype": "text/plain",
    "filetype": "javascript",
    "pretty_type": "JavaScript/JSON",
    "editable": True,
    "size": 28,
    "mode": "snippet",
    "is_external": False,
    "external_type": "",
    "is_public": False,
    "public_url_shared": False,
    "display_as_bot": False,
    "username": "",
    "url_private": "https://files.slack.com/files-pri/T4HRUBFLP-F6GJ9M24F/message.json",
    "url_private_download": "https://files.slack.com/files-pri/T4HRUBFLP-F6GJ9M24F/download/message.json",
    "permalink": "https://appointmentguru.slack.com/files/guru/F6GJ9M24F/message.json",
    "permalink_public": "https://slack-files.com/T4HRUBFLP-F6GJ9M24F-775751e5e7",
    "edit_link": "https://appointmentguru.slack.com/files/guru/F6GJ9M24F/message.json/edit",
    "lines": 1, "lines_more": 0, "preview_is_truncated": False, "channels": [], "groups": [], "ims": [], "comments_count": 0 }