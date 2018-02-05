# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase, override_settings
from services.backends.onesignal import OneSignalBackend
from .helpers import quick_create_push_notification
import responses, json


class OneSignalSendTestCase(TestCase):

    @override_settings(PUSH_BACKEND='services.backends.onesignal.OneSignalBackend')
    @responses.activate
    def setUp(self):
        responses.add(
            responses.POST,
            'https://onesignal.com/api/v1/notifications',
            json = {'id': 'id_goes_here', 'recipients': 2},
            status = 200
        )
        self.comm = quick_create_push_notification(with_save=False)
        self.be = OneSignalBackend()
        self.result = self.be.send(self.comm)

    def test_it_sets_the_backend_correctly(self):
        assert self.result.status_code == 200

    def test_it_sends_the_correct_payload(self):
        payload = json.loads(self.result.request.body)

        expected_results = [
            # (key, value),
            # ("app_id": ".."),
            ("included_segments", ["Test users"]),
            ("headings", {"en": "This is the title"}),
            ("contents", {"en": "This is a test"}),
        ]
        for key, value in expected_results:
            actual = payload.get(key)
            assert actual == value,\
                'Expected {} to be: {}. It was: {}'\
                    .format(key, value, actual)

    def test_it_sends_the_correct_headers(self):
        pass
        # self.comm.refresh_from_db()
        # assert self.comm.backend_used == 'services.backends.onesignal.OneSignalBackend'
        # assert self.comm.backend_message_id == 'id_goes_here'
        # assert self.comm.backend_result.get('recipients') == 2

class OneSignalFetchTestCase(TestCase):

    @override_settings(ONESIGNAL_APP_ID='app_id')
    @responses.activate
    def test_it_fetches_a_notification(self):
        responses.add(
            responses.GET,
            'https://onesignal.com/api/v1/notifications/some-id?app_id=app_id',
            json = {'id': 'some-id'},
            status = 200
        )
        be = OneSignalBackend()
        result = be.fetch('some-id')
        assert result.status_code == 200
