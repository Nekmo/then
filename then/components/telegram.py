from __future__ import absolute_import

from dataclasses import dataclass
from pip._vendor import requests

from then.components.base import Component, Message

TELEGRAM_API_URL = 'https://api.telegram.org/bot{token}/{method}'


@dataclass
class TelegramMessage(Message):
    """:class:`TelegramMessage` instance created by :class:`Telegram` component. Create It using::

        from then.components import Telegram

        message = Telegram(...).message(body="My message")
        message.send()

    :arg body: message to send.
    """
    body: str
    component: 'Telegram' = None

    def send(self):
        requests.post(TELEGRAM_API_URL.format(token=self.component.token, method='sendMessage'),
                      data={'chat_id': self.component.to, 'text': self.body})


@dataclass
class Telegram(Component):
    """Create a Telegram instance to send a message to a user or group::

        from then.components import Telegram

        Telegram(token='520604247:ABF0EHnzZxDIQ15Re83iWZojuvja24Exxxx',
                 to='-600503825xxxx')\\
            .send(body='Message to group')

    :param token: Bot Token (use @BotFather).
    :param to: User or Group id.
    """
    token: str
    to: str

    _message_class = TelegramMessage
