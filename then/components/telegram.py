from __future__ import absolute_import

from dataclasses import dataclass
from pip._vendor import requests

from then.components.base import Component, Message

TELEGRAM_API_URL = 'https://api.telegram.org/bot{token}/{method}'


@dataclass
class TelegramMessage(Message):
    body: str
    component: 'Telegram' = None

    def send(self):
        requests.post(TELEGRAM_API_URL.format(token=self.component.token, method='sendMessage'),
                      data={'chat_id': self.component.to, 'text': self.body})


@dataclass
class Telegram(Component):
    token: str
    to: str

    _message_class = TelegramMessage
