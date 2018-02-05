from django.core import mail
from weasyprint import HTML
from django.conf import settings
from anymail.message import AnymailMessage
import json, six


class Email:

    def __init__(self, to, frm=settings.DEFAULT_FROM_EMAIL):
        self.to = to
        self.frm = frm

    def send(self, subject, plaintext, html, urls=[], tags=[]):
        message = AnymailMessage(
                    subject,
                    plaintext,
                    self.frm,
                    self.to,
                    tags=tags)
        if len(tags) > 0:
            message.metadata = tags

        for index, url in enumerate(urls):
            pdf = HTML(url).write_pdf()
            formatted_name = 'attachment-{}.pdf'.format(index+1)
            message.attach(formatted_name, pdf, 'application/pdf')

        message.track_clicks = True
        message.attach_alternative(html, "text/html")
        result =  message.send()
        return (result, message)

    def send_html_email(self, subject, plaintext, html):
        return mail.send_mail(subject, plaintext, self.frm, self.to, html_message=html)

    def update_status(self, original_communication, payload, **kwargs):
        if isinstance(payload, six.string_types):
            payload = json.loads(payload)

        from api.models import CommunicationStatus
        status = CommunicationStatus()
        status.communication = original_communication
        status.status = payload.get('event')
        status.raw_result = payload
        status.save()
        return status

    def status_update(self, payload):
        '''
        @deprecated
        '''

        # normalize:
        if isinstance(payload, six.string_types):
            payload = json.loads(payload)

        from api.models import CommunicationStatus, Communication
        from api.models import CommunicationStatus
        status = CommunicationStatus()

        message_id = payload.get('Message-Id')
        if message_id is not None:
            try:
                comm = Communication.objects.get(backend_message_id=message_id)
                status.communication = comm
            except Communication.DoesNotExist:
                pass
        status.status = payload.get('event')
        status.save()

        status.raw_result = payload
        status.save()
        return status

    def reply_received(self, payload):
        """
        Handle a reply to an incoming email
        """
        # create communication message
        #
        pass

    def get_id_from_payload(self, payload):
        # TODO: Get Message ID
        return payload.get('Message-Id')

class GoogleActions:

    def goto(self):

        template = """
<div itemscope itemtype="http://schema.org/EmailMessage">
<div itemprop="potentialAction" itemscope itemtype="http://schema.org/ViewAction">
<link itemprop="target" href="https://watch-movies.com/watch?movieId=abc123"/>
<meta itemprop="name" content="Watch movie"/>
</div>
<meta itemprop="description" content="Watch the 'Avengers' movie online"/>
</div>
        """
