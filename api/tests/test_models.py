# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from ..models import Communication, CommunicationTemplate, CommunicationStatus
from .datas.payloads import ZOOMCONNECT_REPLY_PAYLOAD
from .testutils import quick_create_sms

from django.test import TestCase, override_settings
from django.contrib.auth import get_user_model
from django.core import mail

import json, responses

@override_settings(SMS_BACKEND='services.backends.mocksms.MockSMSBackend')
@override_settings(CELERY_ALWAYS_EAGER=True)
class CommunicationModelCreatedTestCase(TestCase):

    def setUp(self):
        self.sms = quick_create_sms()

    def test_it_adds_tags_to_message(self):
        pass


@override_settings(CELERY_ALWAYS_EAGER=True)
class ModelAppliesTemplateTestCase(TestCase):

    def setUp(self):

        self.user = get_user_model().objects.create_user(username='joe')
        data = {
            "owner": self.user,
            "subject": "hi {{first_name}}",
            "short_message": "This is a short message: {{foo}}",
            "message": "This is a long message: {{foo}}"
        }
        self.tmplt = CommunicationTemplate.objects.create(**data)

        data = {
            "template": self.tmplt,
            "context": {"first_name": "Joe", "foo": "bar"}
        }
        self.comms = Communication.objects.create(**data)
        self.comms.apply_template()

    def test_it_templates_subject(self):
        assert self.comms.subject == 'hi Joe'

    def test_it_templates_short_message(self):
        expected_message = '<p>This is a short message: bar</p>'
        self.assertHTMLEqual(self.comms.short_message, expected_message)
        # assert self.comms.short_message == expected_message,\
        #     'Expected: {}. Got: {}'.format(expected_message, self.comms.short_message)

    def test_it_templates_message(self):
        expected_message = '<p>This is a long message: bar</p>'
        self.assertHTMLEqual(self.comms.message, expected_message)
        # assert self.comms.message == expected_message,\
        #     'Expected: {}. Got: {}'.format(expected_message, self.comms.message)

    def test_as_json_string(self):
        res = self.comms.as_json_string
        assert isinstance(res, str)
        json.loads(res) # verify it's valid json

@override_settings(CELERY_ALWAYS_EAGER=True)
class ModelSendsEmailWithAttachmentsTestCase(TestCase):

    def setUp(self):
        data = {
            "owner": '1',
            "subject": "Sending webpage as attachment",
            "message": "Please find attached",
            "sender_email": "christo@appointmentguru.co",
            "recipient_emails": ["info@38.co.za", "christo@cretivecolibri.com"],
            "attached_urls": ['http://google.com']
        }
        self.comm = Communication.objects.create(**data)

    def test_is_adds_attachment(self):
        assert len(mail.outbox[0].attachments) == 1

    def test_it_sets_message_id(self):
        self.comm.refresh_from_db()
        # todo .. verify that it's saving the response ..

@override_settings(CELERY_ALWAYS_EAGER=True)
class ModelSendsSMSTestCase(TestCase):

    def setUp(self):
        pass

    @responses.activate
    @override_settings(ZOOM_BASE_URL='https://www.zoomconnect.com:443')
    @override_settings(ZOOM_API_TOKEN='1234')
    @override_settings(ZOOM_EMAIL='joe@soap.com')
    @override_settings(SMS_BACKEND='services.backends.zoomconnect.ZoomSMSBackend')
    def test_sets_zoom_connect_backend_details(self):

        responses.add(
            responses.POST,
            'https://www.zoomconnect.com:443/app/api/rest/v1/sms/send',
            json = {'messageId': '5a76e8167736b6c1d341643e', 'error': None}
        )

        sms = quick_create_sms()
        assert sms.backend_used == 'services.backends.zoomconnect.ZoomSMSBackend'
        assert sms.backend_message_id == '5a76e8167736b6c1d341643e'
        assert sms.backend_result.get('messageId') == '5a76e8167736b6c1d341643e'

class CommunicationGetZoomConnectFromPayloadTestCase(TestCase):
    """
    Refactor: I guess this should really be in test_zoombackend ?
    """

    def setUp(self):
        self.comm = Communication()
        self.comm.backend_message_id = "5a757f2a7736b6c1d340a1a4"
        self.comm.recipient_phone_number = '+27832566533'
        self.comm.backend_used = "zoomconnect"
        self.comm.short_message = 'testing'
        self.comm.object_ids = ['user:1']
        self.comm.cancel_signal = True
        self.comm.owner = '1'
        self.comm.save()

        self.status_payload = {
            "messageId": "5a757f2a7736b6c1d340a1a4",
            "status": 'DELIVERED',
        }
        self.reply_payload = {
            "dataField": "msg:{}".format(self.comm.id)
        }

    def test_get_from_status_payload(self):
        '''
        this doesnt pass
        '''
        old_comm = Communication.get_from_payload(
            'zoomconnect',
            'sms',
            self.status_payload
        )
        assert old_comm.id is self.comm.id

    def test_get_from_status_payload(self):
        old_comm = Communication.get_from_payload(
            'zoomconnect',
            'sms',
            self.status_payload
        )
        assert old_comm.id is self.comm.id
