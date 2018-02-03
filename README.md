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


# todo:

* Define a scenario (e.g.: Appointment created, Appointment rescheduled etc.) which creates a configured collection of communications

User has Scenarios have Communications
User has Communications