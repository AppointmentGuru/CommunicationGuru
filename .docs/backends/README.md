## Backends

> A backend is a pluggable module which exposes a specific API which CommunicationGuru can use to perform all the tasks it needs.

### Example Usage

A backend should implement the following interface:

#### Send

```python
backend = MyBackend(communication)
# backend.is_valid() is typically called in send, so there is no need to call it here
if backend.is_valid():
    backend.send()
```


## SMS

### ZoomConnect

### Twillio

(partial support)

## E-mail

### Mailgun

## In-App Notifications

### OneSignal

## Other

### PubNub