from django.conf import settings
from django.utils.module_loading import import_string
from phonenumbers import PhoneNumber

class SMS:

    def __init__(self):
        self.sms = import_string(settings.SMS_BACKEND)()

    def send(self, message, to):
        # normalize to text repo of phone number:
        if isinstance(to, PhoneNumber):
            to = to.as_e164

        if settings.SANDBOX_MODE:
            message = "[SANDBOX for: {}] {}" . format(to, message)
            to = settings.SANDBOX_SMS

        return self.sms.send(message, to)

    def save(self, communication, result):
        self.sms.save(communication, result)

    def status_update(self, payload):
        self.sms.status_update(payload)