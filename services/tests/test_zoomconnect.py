from services.backends.zoomconnect import ZoomSMSBackend
from api.models import Communication, CommunicationStatus
from services.sms import SMS

from .datas import ZOOMCONNECT_REPLY_PAYLOAD, ZOOMCONNECT_STATUS_UPDATE
from .helpers import quick_create_sms

from django.test import TestCase, override_settings
from django.conf import settings

import responses, json
from .helpers import quick_create_sms
from .datas import ZOOMCONNECT_STATUS_UPDATE, ZOOMCONNECT_REPLY
# TODO: refactor to backends


@override_settings(SMS_BACKEND='services.backends.zoomconnect.ZoomSMSBackend')
@override_settings(ZOOM_EMAIL='joe@soap.com')
@override_settings(ZOOM_API_TOKEN='1234')
class ZoomSendSMSTestCase(TestCase):

    def __send_sms(self):
        self.sms = ZoomSMSBackend()
        responses.add(
            responses.POST,
            'https://www.zoomconnect.com:443/app/api/rest/v1/sms/send?token=1234&email=joe@soap.com',
            json={"messageId": "456", "error": None}
        )

        return self.sms.send("testing testing 123", "+27730720832")

    @responses.activate
    def test_it_sets_data(self):
        msg = self.__send_sms()

        payload_sent = json.loads(responses.calls[0].request.body.decode('UTF-8'))
        assert payload_sent.get('recipientNumber') == '+27730720832'
        assert payload_sent.get('message') == "testing testing 123"

    @responses.activate
    def test_it_sends_correct_headers(self):
        msg = self.__send_sms()
        headers = responses.calls[0].request.headers
        assert headers.get('Content-type') == 'application/json'
        assert headers.get('Accept') == 'application/json'


@override_settings(SMS_BACKEND='services.backends.zoomconnect.ZoomSMSBackend')
@override_settings(ZOOM_EMAIL='joe@soap.com')
@override_settings(ZOOM_API_TOKEN='1234')
class ZoomTestBackendTestCase(TestCase):

    def __expect_response(self):
        responses.add(
            responses.POST,
            'https://www.zoomconnect.com:443/app/api/rest/v1/sms/send?token=1234&email=joe@soap.com',
            json = {"messageId": "456", "error": None}
        )

    @responses.activate
    def test_send_with_tags_and_campaign(self):
        self.__expect_response()
        sms = SMS()
        res = sms.send(
            'this is a test',
            '+27730720832',
            tags='app:310,pra:684,cli:685,pro:12345',
            campaign='test')


@override_settings(SMS_BACKEND='services.backends.zoomconnect.ZoomSMSBackend')
@override_settings(ZOOM_EMAIL='joe@soap.com')
@override_settings(ZOOM_API_TOKEN='1234')
class ZoomQuerySMSTestCase(TestCase):

    def __expect_response(self, path):
        responses.add(
            responses.GET,
            'https://www.zoomconnect.com:443/app/api/rest{}?token=1234&email=joe@soap.com'.format(path)
        )

    @responses.activate
    def test_fetch(self):
        self.__expect_response('/v1/messages/message_id')
        sms = SMS().fetch('message_id')

    @responses.activate
    def test_search(self):
        params = {
            'dataField': 'pra:1'
        }
        self.__expect_response('/v1/messages/all?dataField=pra%3A1')
        res = SMS().search(params)

class ZoomStatusUpdateTestCase(TestCase):

    def setUp(self):
        self.comm = quick_create_sms(ZOOMCONNECT_STATUS_UPDATE.get('messageId'))
        zc = ZoomSMSBackend()
        zc.update_status(ZOOMCONNECT_STATUS_UPDATE)

    def test_it_creates_communication_status(self):
        self.assertIsInstance(CommunicationStatus.objects.all().first().communication, Communication)
        self.assertEqual(CommunicationStatus.objects.count(), 1)

    def test_communication_status_is_attached_to_original_message(self):
        self.assertEqual(
            CommunicationStatus.objects.all().first().communication,
            self.comm
        )

    def test_communication_status_has_correct_status(self):
        self.assertEqual(
            CommunicationStatus.objects.all().first().status,
            ZOOMCONNECT_STATUS_UPDATE.get('status')
        )

class ZoomReplyUpdateTestCase(TestCase):

    def setUp(self):
        self.comm1 = quick_create_sms('5a75b1e67736b6c1d340af1e')
        zc = ZoomSMSBackend()
        zc.reply_received(self.comm1, ZOOMCONNECT_REPLY)

    def test_communication_created_for_reply(self):
        self.assertEqual(Communication.objects.count(), 2)

    def test_reply_is_attached_to_original_communication(self):
        self.assertEqual(Communication.objects.all().last().related_communication, self.comm1)

    def test_reply_is_ok(self):
        reply_comm = Communication.objects.all().last()
        self.assertEqual(reply_comm.short_message, ZOOMCONNECT_REPLY.get('message'))
        self.assertEqual(reply_comm.recipient_phone_number, ZOOMCONNECT_REPLY.get('from'))
        self.assertEqual(reply_comm.sender_phone_number, self.comm1.sender_phone_number)
