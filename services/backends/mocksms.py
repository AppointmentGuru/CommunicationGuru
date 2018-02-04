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
import uuid

class MockSMSBackend:

    def __init__(self):
        pass

    def send(self, message, to, **kwargs):
        return {'message': message, 'to': to}

    @staticmethod
    def get_id_from_payload(payload, always_return_id=1):
        return always_return_id

    def update_status(self, communication, payload, **kwargs):
        data = {
            'communication': communication,
            'payload': payload
        }
        id = str(uuid.uuid4())
        return (id, data)

    def reply_received(self, original_communication, payload, *args, **kwargs):
        return {
            'original_communication': original_communication,
            'payload': payload
        }
