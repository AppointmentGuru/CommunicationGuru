from django.test import TestCase
import json


class WebHookTestCase(TestCase):

    def test_slack_webhook_payload(self):

        data = {
            "foo": "bar",
            "baz": "bus",
            "event": "delivered"
        }
        result = self.client.post('/incoming/slack/', json.dumps(data), content_type='application/json')
        assert result.status_code == 200
        import ipdb;ipdb.set_trace()