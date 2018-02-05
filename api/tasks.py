from django.conf import settings
from services.sms import SMS
from services.email import Email
from celery import shared_task
import json
from .models import Communication

@shared_task
def ping():
    return {'result': 'pong'}

@shared_task
def send_sms(communication):
    '''
    Sends an SMS based off a provided communication
    '''
    sms = SMS()
    if isinstance(communication, str):
        communication = json.loads(communication)
    message = communication.get('short_message')
    recipient = communication.get('recipient_phone_number')
    result = sms.send(message, recipient)
    return result

@shared_task
def send_email(communication):
    '''
    Sends an email based on the provided communication
    '''
    if isinstance(communication, str):
        communication = json.loads(communication)

    recipients = communication.get('recipient_emails')
    sender = communication.get('sender_email')
    subject = communication.get('subject')
    message = communication.get('message')
    urls = communication.get('attached_urls')
    emailer = Email(recipients, sender)

    result, message = emailer.send(subject, message, message, urls=urls)
    response = {
        "result": result
    }
    status = message.anymail_status
    comm_id = communication.get('id', None)
    if comm_id is not None and status is not None:
        communication = Communication.objects.get(id=comm_id)
        communication.backend_used = settings.EMAIL_BACKEND
        communication.backend_message_id = status.message_id
        if status.esp_response is not None:
            communication.backend_result = message.anymail_status.esp_response.json()
            response["response"] = message.anymail_status.esp_response.json()
        communication.save()

        response["message_id"] = status.message_id

    return response


# example sms response
# {
# 	'parent': < twilio.rest.resources.messages.Messages object at 0x7fc08a57a2e8 > ,
# 	'name': '..',
# 	'base_uri': 'https://api.twilio.com/2010-04-01/Accounts/.../Messages',
# 	'auth': ('..', '..'),
# 	'timeout': < Unset Timeout Value > ,
# 	'sid': 'SMb2c6f00d73c94ed7beb85f6774c4290d',
# 	'date_created': datetime.datetime(2017, 11, 13, 22, 6, 3),
# 	'date_updated': datetime.datetime(2017, 11, 13, 22, 6, 3),
# 	'date_sent': None,
# 	'account_sid': '..',
# 	'to': '+27832566533',
# 	'messaging_service_sid': None,
# 	'body': '[SANDBOX for: +27832566533] testing',
# 	'status': 'queued',
# 	'num_segments': '1',
# 	'num_media': '0',
# 	'direction': 'outbound-api',
# 	'api_version': '2010-04-01',
# 	'price': None,
# 	'price_unit': 'USD',
# 	'error_code': None,
# 	'error_message': None,
# 	'subresource_uris': {
# 		'media': '/2010-04-01/Accounts/../Messages/../Media.json'
# 	},
# 	'from_': '+12019044071',
# 	'media_list': < twilio.rest.resources.media.MediaList object at 0x7fc08a57ac50 >
# }