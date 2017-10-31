'''
Helpers. For getting stuff done
'''
from .models import Communication
from weasyprint import HTML
from django.conf import settings
import requests

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

