from django.test import TestCase

from ..helpers import msg, email_with_webpage_screenshots

class HelpersTestCase(TestCase):

    # def test_minimal_send_sms_msg(self):
    #     msg('testing', '+27832566533')

    def test_email_with_webpage_screenshots(self):

        result = email_with_webpage_screenshots(
            ['christo@appointmentguru.co', 'christo@creativecolibri.com'],
            'tech@appointmentguru.co',
            'Screenshots of search engines',
            'Attached please find screenshots of google, yahoo and bing',
            [('http://google.com', 'google'),
            ('http://bing.com', 'bing'),
            ('http://yahoo.com', 'yahoo')]
        )
        import ipdb;ipdb.set_trace()