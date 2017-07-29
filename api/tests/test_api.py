from django.test import TestCase
import json

class WebHookTestCase(TestCase):

    def test_slack_webhook_payload(self):

        data = {
            "foo": "bar",
            "baz": "bus"
        }
        result = self.client.post('/incoming/slack/', json.dumps(data), content_type='application/json')
