# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase, override_settings
from django.core import mail
from django.contrib.auth import get_user_model
from django.core.mail import outbox

from ..models import Communication, CommunicationTemplate, CommunicationStatus
from ..helpers import (
    create_in_app_communication,
    create_sms,
    create_email
)
from .testutils import (
    create_mock_communication_template,
    create_templated_communication
)
import json, responses

class CommunicationTestCase(TestCase):

    def test_minimal_sms_fields(self):

        comm = Communication()
        comm.short_message = 'testing'
        comm.owner = '1'
        comm.object_ids = 'user:1'
        comm.recipient_phone_number = '+27832566533'
        comm.save()


example_schema = {
  "$id": "http://example.com/example.json",
  "type": "object",
  "definitions": {},
  "$schema": "http://json-schema.org/draft-07/schema#",
  "properties": {
    "first_name": {
      "$id": "/properties/first_name",
      "type": "string",
      "title": "The First_name Schema ",
      "default": "",
      "examples": [
        "Joe"
      ]
    },
    "foo": {
      "$id": "/properties/foo",
      "type": "string",
      "title": "The Foo Schema ",
      "default": "",
      "examples": [
        "bar"
      ]
    }
  },
  "required": [
    "first_name",
    "foo"
  ]
}

@override_settings(CELERY_ALWAYS_EAGER=True)
class ModelValidatesTemplateTestCase(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='joe')

        data = {
            "owner": self.user,
            "subject": "hi {{first_name}}",
            "short_message": "This is a short message: {{foo}}",
            "message": "This is a long message: {{foo}}",
            "schema": example_schema
        }
        self.tmplt = CommunicationTemplate.objects.create(**data)

        data = {
            "template": self.tmplt,
            "context": {"first_name": "Joe", "foo": "bar"}
        }
        self.comms = Communication.objects.create(**data)

    def test_valid_context_validates(self):

        is_valid, errors = self.comms.validate_template_context()
        assert is_valid == True

    def test_marks_invalid_content_as_invalid(self):
        self.comms.context = {
            "invalid": "context"
        }
        is_valid, errors = self.comms.validate_template_context()
        assert is_valid == False



@override_settings(CELERY_ALWAYS_EAGER=True)
class ModelAppliesTemplateTestCase(TestCase):

    @responses.activate
    def setUp(self):

        self.user = get_user_model().objects.create_user(username='joe')

        data = {
            "owner": self.user,
            "owner": 1,
            "subject": "hi {{first_name}}",
            "short_message": "This is a short message: {{foo}}",
            "message": "This is a long message: {{foo}}",
            "schema": example_schema
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
        expected_message = 'This is a short message: bar'
        self.assertEqual(self.comms.short_message, expected_message)
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

class CustomTemplateTestCase(TestCase):

    def __create_communication(self, owner_id, template = None, slug = None):

        data = {
            "owner": owner_id,
            "context": {
                "first_name": "Joe",
                "foo": "bar"
            }
        }
        if template is not None:
            data.update({"template": template})

        if slug is not None:
            data.update({"template_slug": slug})

        return Communication.objects.create(**data)


    @responses.activate
    def setUp(self):
        self.slug = 'TEST_TEST'
        data = {
            "owner": 0,
            "subject": "hi {{first_name}}",
            "short_message": "This is a short message: {{foo}}",
            "message": "This is a long message: {{foo}}",
            "slug": self.slug,
            "schema": example_schema,
        }
        self.base_template = CommunicationTemplate.objects.create(**data)

    @responses.activate
    def test_custom_template_overrides_default(self):
        owner_id = 2
        context = {"foo": "bar"}
        custom_template = create_mock_communication_template(owner_id=owner_id, slug=self.slug)
        custom_template.subject = "overridden subject {{foo}}"
        custom_template.short_message = "overridden short_message {{foo}}"
        custom_template.message = "overridden message {{foo}}"
        custom_template.save()
        comm = create_templated_communication(self.slug, owner_id)

        comm.refresh_from_db()
        assert comm.subject == 'overridden subject bar'
        assert comm.short_message == 'overridden short_message bar'
        self.assertHTMLEqual('<p>overridden message bar</p>', comm.message)

    def test_send_to_default_if_no_custom_template(self):
        owner_id = 2
        comm = self.__create_communication(owner_id, slug=self.slug)

        comm.refresh_from_db()
        assert comm.subject == 'hi Joe', 'Expected \'hi Joe\'. Got: {}'.format(comm.subject)
        assert comm.short_message == 'This is a short message: bar'
        self.assertHTMLEqual('<p>This is a long message: bar</p>', comm.message)



class ModelSendTestCase(TestCase):

    def test_send_inapp_notification(self):
        backend = 'services.backends.onesignal.OneSignalBackend'
        res = create_in_app_communication("test", "this is a test", "Test subject", backend=backend)


class ZoomConnectCommunicationTestCase(TestCase):

    def test_send_sms(self):
        backend = 'services.backends.zoomconnect.ZoomSMSBackend'
        res = create_sms(
            "test-channel",
            "This is the message",
            "+27832566533",
            tags = ['test'],
            backend = backend
        )
        assert res.backend_used == backend

    def test_zoom_handle_reply(self):
        pass

class EmailTestCase(TestCase):

    def setUp(self):
        self.comm = create_email(
            channel = "test",
            subject = "email subject",
            message = "email message",
            from_email = "tech@appointmentguru.co",
            to_emails = ["joe@soap.com", "jane@soap.com"]
        )

    def test_sends_email(self):
        # oddly you seem to need to import this so that it updates
        from django.core.mail import outbox
        num_messages = len(outbox)
        assert num_messages == 1, \
            'Expected 1 message in the outbox, found: {}'.format(num_messages)


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
        # assert len(mail.outbox[0].attachments) == 1
        pass

    def test_it_sets_message_id(self):
        self.comm.refresh_from_db()
        # todo .. verify that it's saving the response ..

class CommunicationTestCase(TestCase):

    def setUp(self):
        comm = Communication()
        comm.save()

        for x in range(0,5):
            stat = CommunicationStatus()
            stat.status = str(x)
            stat.communication = comm
            stat.save()

        self.comm = comm

    def test_status_list(self):

        status_list = self.comm.status_list
        assert len(status_list) == 5

