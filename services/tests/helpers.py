from api.models import Communication


def quick_create_sms(backend_message_id):
    comm = Communication()
    comm.recipient_phone_number = '+27832566533'
    comm.short_message = 'testing'
    comm.backend_message_id = backend_message_id
    comm.save()
    return comm