from __future__ import absolute_import

from email.message import EmailMessage as MimeEmailMessage
from smtplib import SMTP

from then.components.base import ConfigBase, TemplateBase, MessageBase, split_host_port
from then.types import EmailType, CharType


class EmailMessage(MessageBase):
    def __init__(self, subject, body):
        super(EmailMessage, self).__init__(**self.get_init_data(locals()))


class EmailTemplate(TemplateBase):
    subject = CharType
    body = CharType

    message_class = EmailMessage


class EmailConfig(ConfigBase):
    to = EmailType(required=True)  # TODO: multiple dests
    from_ = EmailType(default='noreply@localhost')
    server = CharType(default='localhost')

    def __init__(self, **kwargs):
        super(EmailConfig, self).__init__(**kwargs)
        self.message = MimeEmailMessage()
        self.server, self.port = split_host_port(self.server, 0)
        self.message['From'] = self.from_
        self.message['To'] = self.to

    def send(self, subject, body, type='text/plain'):
        self.message['Subject'] = subject
        if body:
            self.message.set_content(body)
            self.message.set_type(type)
        s = SMTP(self.server, self.port)
        s.send_message(self.message, self.from_, self.to)
        s.quit()
