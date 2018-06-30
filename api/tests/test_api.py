from django.test import TestCase, override_settings
from django.conf import settings
import json, responses

from .datas.payloads import TWILLIO_SMS_SENT, MAILGUN_STATUS_UPDATE
from ..models import CommunicationStatus, Communication
from .testutils import assert_response, get_proxy_headers
from services.backends.zoomconnect import ZoomSMSBackend
from services.backends.generators.zoomconnect import (
    reply as mock_zoom_reply
)
from api.helpers import create_sms
from django.urls import reverse

import unittest

@override_settings(DEFAULT_SHORT_MESSAGE_BACKEND='services.backends.mockbackend.MockShortMessageBackend')
@override_settings(SMS_BACKEND='services.backends.zoomconnect.ZoomSMSBackend')
@override_settings(ZOOM_EMAIL='joe@soap.com')
@override_settings(ZOOM_API_TOKEN='1234')
class IncomingReplyTestCase(TestCase):

    def __mock_send_sms(self):
        responses.add(
            responses.POST,
            'https://www.zoomconnect.com:443/app/api/rest/v1/sms/send?token=1234&email=joe@soap.com',
            json = {"messageId": "456", "error": None}
        )

    @responses.activate
    def setUp(self):
        self.__mock_send_sms()
        self.backend_name = 'services.backends.zoomconnect.ZoomSMSBackend'
        self.comm = create_sms(
            "test-channel",
            "This is the message",
            "+27832566533",
            tags = ['test'],
            backend = self.backend_name
        )
        data = {
            "messageId": self.comm.backend_message_id
        }
        self.be = ZoomSMSBackend.from_payload(self.backend_name, data)

    @responses.activate
    def test_incoming_zoom_reply(self):

        data = mock_zoom_reply()
        url = reverse('incoming_message', args=('services.backends.zoomconnect.ZoomSMSBackend',))
        res = self.client.post(url, data)

        assert res.status_code == 200
        Communication.objects.count() == 2
        Communication.objects.last().backend_used == settings.DEFAULT_SHORT_MESSAGE_BACKEND


class WebHookTestCase(TestCase):

    def test_slack_webhook_payload(self):

        data = {
            "X-Mailgun-Sid": '123',
            "foo": "bar",
            "baz": "bus",
            "event": "delivered"
        }
        result = self.client.post('/incoming/slack/', json.dumps(data), content_type='application/json')
        assert_response(result)

    def test_mailgun_status_update(self):

        result = self.client.post('/incoming/slack/', json.dumps(MAILGUN_STATUS_UPDATE), content_type='application/json')
        assert_response(result)
        assert CommunicationStatus.objects.count() == 1,\
            'Expect it to create a communication status'

    def test_get_data(self):
        result = self.client.post('/incoming/slack/?foo=bar', content_type='application/json')
        assert result.status_code == 200

@unittest.skip('Not currently supported')
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

# class SMSMessageSearchEndPointTestCase(TestCase):

#     @override_settings(SMS_BACKEND='services.backends.twillio.TwillioBackend')
#     def test_403_error_if_backend_doesnt_support_search(self):
#         url = reverse('backend_messages', args=('sms',))

#         response = self.client.get(url, **get_proxy_headers("1"))
#         assert_response(response, 403)

#     @responses.activate
#     @override_settings(SMS_BACKEND='services.backends.zoomconnect.ZoomSMSBackend')
#     @override_settings(ZOOM_BASE_URL='https://www.zoomconnect.com:443')
#     @override_settings(ZOOM_API_TOKEN='1234')
#     @override_settings(ZOOM_EMAIL='joe@soap.com')
#     @override_settings(SMS_BACKEND='services.backends.zoomconnect.ZoomSMSBackend')
#     def test_performs_search(self):
#         responses.add(
#             responses.GET,
#             'https://www.zoomconnect.com:443/app/api/rest/v1/messages/all?fieldData=foo&campaign=practitioner-1&email=joe%40soap.com&token=1234',
#             json = {"messages": []}
#         )
#         url = reverse('backend_messages', args=('sms',))
#         url = '{}?fieldData=foo'.format(url)
#         response = self.client.get(url, **get_proxy_headers("1"))


@override_settings(CELERY_ALWAYS_EAGER=True)
class CreateEmailCommunicationTestCase(TestCase):

    def setUp(self):
        data = {
            "object_ids": ['object:1'],
            "subject": 'test',
            "message": 'this is a test',
            "preferred_transport": 'email',
            "attached_urls": ['https://google.com'],
            "recipient_emails": ['info@38.co.za'],
            "sender_email": 'christo@appointmentguru.co'
        }
        owner_id = "1"
        url = reverse('communication-list')
        self.result = self.client.post(url, data, **get_proxy_headers(owner_id))
        self.owner_id = owner_id

    def test_result_is_ok(self):
        assert_response(self.result, 201)

    def test_communication_has_owner_set(self):
        comm = Communication.objects.first()
        assert comm.owner == self.owner_id,\
            'Expected owner to be: "{}". got: "{}"'.format(self.owner_id, comm.owner)
