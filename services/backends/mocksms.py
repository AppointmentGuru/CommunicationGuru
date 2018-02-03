"""
A mock backend to be used in testing.

Typically, you'll want to decorate your TestCase or method with:

@override_settings(SMS_BACKEND='services.backends.mocksms.MockSMSBackend')

for mocking:

```
from services.backends.mocksms import MockSMSBackend
@mock.patch.object(MockSMSBackend, 'send')
def test_something(self, mock_sms)
    ...
```
"""

from twilio.rest import TwilioRestClient
from django.conf import settings

class MockSMSBackend:

    def __init__(self):
        pass

    def send(self, message, to, **kwargs):
        return {'message': message, 'to': to}

    @staticmethod
    def get_id_from_payload(payload):
        pass

    def update_status(self, payload):
        return {
            'payload': payload
        }

    def reply_received(self, original_message, payload):
        return {
            'original_message': original_message,
            'payload': payload
        }
