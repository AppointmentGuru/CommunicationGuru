# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase, override_settings
from django.core import mail
from django.contrib.auth import get_user_model
from ..models import Communication, CommunicationTemplate
import json

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
        assert self.comms.short_message == 'This is a short message: bar'

    def test_it_templates_message(self):
        assert self.comms.message == 'This is a long message: bar'

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
        import ipdb;ipdb.set_trace()

