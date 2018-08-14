from __future__ import absolute_import

from email.message import EmailMessage as MimeEmailMessage
from smtplib import SMTP

from then.components.base import split_host_port, Component, Message
from then.types import EmailType
from dataclasses import dataclass


@dataclass
class EmailMessage(Message):
    subject: str = ''
    body: str = ''
    component: 'Email' = None

    def __post_init__(self):
        self.message = MimeEmailMessage()
        self.message['From'] = self.component.from_
        self.message['To'] = self.component.to
        if self.body:
            self.message['Subject'] = self.subject
        if self.body:
            self.message.set_content(self.body)
            self.message.set_type(self.component.mode)

    def send(self):
        server, port = split_host_port(self.component.server, 0)
        s = SMTP(server, port)
        s.send_message(self.message, self.component.from_, self.component.to)
        s.quit()


@dataclass
class Email(Component):
    to: str
    from_: str = 'noreply@localhost'
    server: str = 'localhost'
    mode: str = 'text/plain'

    _message_class = EmailMessage

    class Validate:
        to = EmailType()
        from_ = EmailType()
