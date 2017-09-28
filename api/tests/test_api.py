from django.test import TestCase
import json

from .datas.payloads import TWILLIO_SMS_SENT, MAILGUN_STATUS_UPDATE
from ..models import CommunicationStatus

class WebHookTestCase(TestCase):

    def test_slack_webhook_payload(self):

        data = {
            "X-Mailgun-Sid": '123',
            "foo": "bar",
            "baz": "bus",
            "event": "delivered"
        }
        result = self.client.post('/incoming/slack/', json.dumps(data), content_type='application/json')
        assert result.status_code == 200

    def test_mailgun_sttus_update(self):

        result = self.client.post('/incoming/slack/', json.dumps(MAILGUN_STATUS_UPDATE), content_type='application/json')
        assert result.status_code == 200


class IncomingTwillioSMSWebHookTestCase(TestCase):

    def setUp(self):

        self.result = self.client.post(
            '/incoming/slack/',
            json.dumps(TWILLIO_SMS_SENT),
            content_type='application/json')

    def assert_is_ok(self):
        assert self.result.status_code == 200

    def test_incoming_twillio_sms_result(self):
        assert CommunicationStatus.objects.count() == 1
