from __future__ import absolute_import

import re
from email.message import EmailMessage as MimeEmailMessage
from smtplib import SMTP, SMTP_SSL
from typing import Union, List, Tuple

from then.components.base import split_host_port, Component, Message
from then.types import EmailType
from dataclasses import dataclass


DEFAULT_SERVER = 'localhost'
DEFAULT_CONFIGS: List[Tuple[Union[str, re.Pattern], dict]] = [
    ('gmail.com', {'tls': True, 'server': 'smtp.gmail.com:465'}),
    (re.compile(r'yahoo\.[a-z]{2,4}', re.IGNORECASE), {'tls': True, 'server': 'smtp.mail.yahoo.com:587'}),
]
DEFAULT_CONFIGS += [
    (re.compile(domain + r'\.[a-z]{2,4}', re.IGNORECASE), {'tls': True, 'server': 'smtp-mail.outlook.com:587'})
    for domain in ['hotmail', 'outlook']
]


def get_default_config(address) -> Union[dict, None]:
    server = address.split('@')[1]
    for config in DEFAULT_CONFIGS:
        if isinstance(config[0], str) and config[0] == server:
            return config[1]
        elif isinstance(config[0], re.Pattern) and config[0].match(server):
            return config[1]


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
        if self.component.tls:
            s = SMTP_SSL(server, port)
        else:
            s = SMTP(server, port)
        if self.component.password:
            s.login(self.component.from_, self.component.password)
        s.send_message(self.message, self.component.from_, self.component.to)
        s.quit()


@dataclass
class Email(Component):
    to: str
    from_: str = 'noreply@localhost'
    server: str = DEFAULT_SERVER
    password: str = None
    tls: Union[bool, None] = None
    mode: str = 'text/plain'

    _message_class = EmailMessage
    _type = 'message'

    def __post_init__(self):
        default_config = get_default_config(self.from_)
        if default_config and self.server == DEFAULT_SERVER:
            self.server = default_config.get('server', DEFAULT_SERVER)
        if default_config and self.tls is None:
            self.tls = default_config.get('tls')
        if self.tls is None:
            self.tls = False

    class Validate:
        to = EmailType()
        from_ = EmailType()
