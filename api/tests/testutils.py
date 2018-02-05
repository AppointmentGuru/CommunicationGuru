# from faker import Factory
# FAKE = Factory.create()
from ..models import Communication

def quick_create_sms(with_save=True):
    comm = Communication()
    comm.recipient_phone_number = '+27832566533'
    comm.owner = '1'
    comm.object_ids = ['user:1']
    comm.short_message = 'testing'
    comm.preferred_transport = 'sms'
    if with_save:
        comm.save()
    return comm

def quick_create_email(with_save=True):
    comm = Communication()
    comm.owner = '1'
    comm.object_ids = ['user:1']
    comm.recipient_emails = ['joe@soap.com']
    comm.sender_email = 'jane@soap.com'
    comm.subject = 'testing'
    comm.message = 'this is a test'
    comm.preferred_transport = 'email'
    if with_save:
        comm.save()
    return comm

def assert_response(response, expected_status=200):
    assert response.status_code == expected_status, \
        'Expected status: {}. Got: {}. {}'.format(expected_status, response.status_code, response.content)

def get_proxy_headers(user_id, consumer='joesoap', headers = {}):
    is_anon = user_id is None
    headers.update({
        'HTTP_X_ANONYMOUS_CONSUMER': is_anon,
        'HTTP_X_AUTHENTICATED_USERID': user_id,
        'HTTP_X_CONSUMER_USERNAME': consumer
    })
    headers['HTTP_X_CONSUMER_USERNAME'] = consumer

    if user_id is None:
        headers['HTTP_X_ANONYMOUS_CONSUMER'] = 'true'
    else:
        headers['HTTP_X_AUTHENTICATED_USERID'] = str(user_id)
    return headers


