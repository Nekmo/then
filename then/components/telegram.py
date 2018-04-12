from __future__ import absolute_import

from pip._vendor import requests

from then.components.base import MessageBase, TemplateBase, ConfigBase
from then.types import CharType

TELEGRAM_API_URL = 'https://api.telegram.org/bot{token}/{method}'


class TelegramMessage(MessageBase):
    def __init__(self, body=''):
        super(TelegramMessage, self).__init__(**self.get_init_data(locals()))


class EmailTemplate(TemplateBase):
    body = CharType

    message_class = TelegramMessage


class TelegramConfig(ConfigBase):
    token = CharType(required=True)
    to = CharType(required=True)

    def send(self, body=''):
        requests.post(TELEGRAM_API_URL.format(token=self.token, method='sendMessage'),
                      data={'chat_id': self.to, 'text': body})
