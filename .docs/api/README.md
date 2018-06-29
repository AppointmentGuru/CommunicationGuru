# API

::: warning
This is a work in progress
:::


## Helpers

> Helpers provide a high level human friendly interface to creating models with the required configurations to send various types of messages

``` python
from communication.helpers import *
```

### `send_sms()`

Sends an SMS

**Usage:**

``` python
send_sms(to='+27...', messaage='...', channel='...')
```

* Channel is optional

### `send_email()`

Sends an Email

**Usage:**

``` python
send_email(subject, message, message, urls=urls)
```

### `send_notification()`

Sends an in app notification

**Usage:**

``` python
send_notification(
    messaage='...',
    channel='...',
    fallback_to_sms=False,
    phone_number=False,
    deliver_to_fallback_timeout_in_seconds=300
)
```

* If `fallback_to_sms` is `True`, then it will initially try send an in-app notification. If the notification is not delivered to _any_ devices within `deliver_to_fallback_timeout_in_seconds`, then it will try send an SMS

### `send_short_message()`

Sends a short message.:

```
..
```

## Sending messages with models

### Try send a communication over In App notification. If that fails, send SMS
```python

communication = Communication()
communication.preferred_transports = ['services.backends.onesignal.OneSignal', '..']
communication.backup_transports = ['services.backends.zoomconnect.ZoomConnect', '..']
communication.recipient_phone_number = '+...'
communication.short_message = 'Hello there!'
```

### ..
```python

communication = Communication()
communication.preferred_transports = ['services.backends.onesignal.OneSignal', '..']
communication.backup_transports = ['services.backends.zoomconnect.ZoomConnect', '..']
communication.recipient_phone_number = '+...'
communication.short_message = 'Hello there!'
```
