'''
Helpers. For getting stuff done
'''
from .models import Communication
import importlib
from django.conf import settings

def get_backend(method_string, communication):
    '''
    given a string path, call the method
    '''
    parts = method_string.split('.') # qualified method: e.g.: api.tasks.ping
    method_to_call = parts.pop()
    module_string = ('.').join(parts)
    module = importlib.import_module(module_string)
    return getattr(module, method_to_call)(communication)

def create_in_app_communication(channel, message, subject, tags=[], backend = None):

    if backend is None:
        backend = settings.DEFAULT_IN_APP_BACKEND

    comm = Communication()
    comm.channel = channel
    comm.backends = [backend]
    comm.short_message = message
    comm.subject = subject
    comm.save()
    comm.send()

    return comm

def create_short_message(channel, message, backend=None, tags = [], **kwargs):

    if backend is None:
        backend = settings.DEFAULT_SHORT_MESSAGE_BACKEND

    comm = Communication()
    comm.channel = channel
    comm.backends = [backend]
    comm.short_message = message
    comm.tags = tags
    comm.subject = kwargs.get('subject')
    comm.recipient_phone_number = kwargs.get('recipient_phone_number')

    comm.save()
    comm.send()

    return comm

def create_sms(channel, message, to, tags=[], backend=None):

    if backend is None:
        backend = settings.SMS_BACKEND

    comm = Communication()
    comm.channel = channel
    comm.backends = [backend]
    comm.short_message = message
    comm.recipient_phone_number = to
    comm.tags = tags
    comm.save()
    comm.send()

    return comm

def send():
    '''Will send any kind of message'''
    pass

def msg(message, number=None, channel=None, owner=None, transports=['sms']):
    '''Send a short message (e.g.: sms, chat, notification etc

    Send an SMS: helpers.msg('message', '+27812345678', owner=1)
    '''
    data = {
        "short_message": message,
        "recipient_phone_number": number
    }
    if 'sms' in transports:
        assert number is not None
        data['recipient_phone_number'] = number

    results = []
    for transport in transports:
        data['preferred_transport'] = transport
        Communication.objects.create(**data)

