'''
A backend for sending email with python AnyMail
'''
import uuid, markdown2
from anymail.message import AnymailMessage
from api.helpers import create_email
from api.models import Communication

def get_id():
    return str(uuid.uuid4())

class EmailBackend:
    backend_id = 'services.backends.email.EmailBackend'

    def __init__(self, communication):
        self.communication = communication

    @classmethod
    def from_payload(cls, backend, data):
        id = data.get('messageId')
        communication = Communication.objects.get(
                            backend_used=backend,
                            backend_message_id=id
                        )
        return cls(communication)

    def __save_result(self, message):
        status = message.anymail_status
        if message:
            self.communication.backend_used = self.backend_id
            self.communication.backend_message_id = status.message_id
            if status.esp_response is not None:
                self.communication.backend_result = status.esp_response.json()
            self.communication.save()

    def send(self):
        urls = []
        comm = self.communication
        message = AnymailMessage(
                    comm.subject,
                    comm.message,
                    comm.sender_email,
                    comm.recipient_emails,
                    tags=comm.tags)
        message.metadata = comm.tags

        html = markdown2.markdown(comm.message)

        for index, url in enumerate(comm.attached_urls):
            pdf = HTML(url).write_pdf()
            formatted_name = 'attachment-{}.pdf'.format(index+1)
            message.attach(formatted_name, pdf, 'application/pdf')

        message.track_clicks = True
        message.attach_alternative(html, "text/html")
        result =  message.send()
        self.__save_result(message)
        return message

    def fetch(self, id, **kwargs):
        pass

    def handle_reply(self, data):
        sender    = data.get('sender')
        recipient = data.get('recipient')
        subject   = data.get('subject', '')

        body_plain = data.get('body-plain', '')
        body_without_quotes = data.get('stripped-text', '')
        # note: other MIME headers are also posted here...

        # attachments:
        # if request.FILES:
        #     for key in request.FILES:
        #         file = request.FILES[key]

        return create_email(
            channel = self.communication.channel,
            subject = subject,
            message = body_plain,
            from_email = sender,
            to_emails=[recipient],
            tags=self.communication.tags
        )

    def receive_status(self, data):
        pass