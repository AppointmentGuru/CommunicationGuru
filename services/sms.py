from django.utils.module_loading import import_string
from phonenumbers import PhoneNumber
from django.conf import settings


class SMS:
    '''
    Deprecated - use Communication model
    '''

    def __init__(self, backend=None):
        if not backend:
            backend = settings.SMS_BACKEND
        self.sms = import_string(backend)()

    def send(self, message, to, **kwargs):
        # normalize to text repo of phone number:
        if isinstance(to, PhoneNumber):
            to = to.as_e164

        if settings.SANDBOX_MODE:
            message = "[SANDBOX for: {}] {}" . format(to, message)
            to = settings.SANDBOX_SMS

        return self.sms.send(message, to, **kwargs)

    def fetch(self, messageId, **kwargs):
        assert getattr(self.sms, 'fetch', None) is not None
        return self.sms.fetch(messageId)

    def search(self, params, **kwargs):
        assert getattr(self.sms, 'search', None) is not None
        return self.sms.search(params, **kwargs)

    def get_id_from_payload(self, payload):
        return self.sms.get_id_from_payload(payload)
