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


# todo: Scenarios

* Define a scenario (e.g.: Appointment created, Appointment rescheduled etc.) which creates a configured collection of communications

User has Scenarios have Communications
User has Communications