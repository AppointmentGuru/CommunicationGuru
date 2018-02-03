# CommunicationGuru
Service for sending communications in a way that is most awesome

## Sending messages:

**Send an SMS**

```
from api.models import Communication
message = Communication.sms(to='+27..', from='+27..', message, tags=[])
```

**Send an Email**

```
from api.models import Communication
message = Communication.email(to='+27..', from='+27..', message, tags=[])
```

## Webhooks:

### Incoming status updates:

`POST /incoming/:transport/:backend/status/`

e.g:

`POST /incoming/email/mailgun/status`

### Incoming replies:

`POST /incoming/:transport/:backend/reply/`

e.g.:

`POST /incoming/email/mailgun/reply`

## Creating a backend:

A backend must implement the following methods:

```
class MyAwesomeBackend:

    def __init__(self):
        pass

    @staticmethod
    def get_id_from_payload(payload, always_return_id=1):
        """
        Given a reply, or status update payload, extract the backend message id
        """

    def send(self, message, to, **kwargs):
        """
        Send a message
        """

    def update_status(self, payload, **kwargs):
        """
        Given a status update payload, update the message status
        """

    def reply_received(self, original_communication, payload, *args, **kwargs):
        """
        Handle a reply to a message
        """

```

# todo: Scenarios

* Define a scenario (e.g.: Appointment created, Appointment rescheduled etc.) which creates a configured collection of communications

User has Scenarios have Communications
User has Communications