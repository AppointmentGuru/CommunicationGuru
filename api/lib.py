'''
Library for easily communicating with CommunicationGuru Service
'''
import requests

class CommunicationGuru:
    '''Wrapper around the CommunicationGuru service making it easy to send communications'''

    def __init__(self, base_url):
        self.base_url = base_url

    def send_email(self, to, subject, message, from_email=None):
        url = '{}/communications/'.format(self.base_url)
        data = {
            'recipient_emails': to,
            'subject': subject,
            'message': message
        }
        if from_email is not None:
            data['sender_email'] = from_email
        return requests.post(url, data)

    def send_sms(self):
        pass

    def send_templated_email(self):
        pass

    def send_templated_sms(self):
        pass

    def send_message(self, preference_order=['sms', 'email']):
        '''Sends a message via the best transport, depending on preferences and information available'''
        pass
