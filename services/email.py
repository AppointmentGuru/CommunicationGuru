from django.core import mail
from django.conf import settings
from anymail.message import AnymailMessage

class Email:

    def __init__(self, to, frm=settings.DEFAULT_FROM_EMAIL):
        self.to = to
        self.frm = frm

    def send(self, subject, plaintext, html, tags=[]):
        message = AnymailMessage(
                    subject,
                    plaintext,
                    self.frm,
                    self.to,
                    tags=tags)
        if len(tags) > 0:
            message.metadata = tags
        message.track_clicks = True
        message.attach_alternative(html, "text/html")
        return message.send()

    def send_html_email(self, subject, plaintext, html):
        return mail.send_mail(subject, plaintext, self.frm, self.to, html_message=html)

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
