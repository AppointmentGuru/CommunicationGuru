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

class MockSMSBackend:

    def __init__(self):
        pass

    def send(self, message, to_number, **kwargs):
        return {'message': message, 'to': to_number}

    def save(self, communication, result, **kwargs):
        return (communication, result)
