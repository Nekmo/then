from __future__ import absolute_import

from dataclasses import dataclass

from then.components.http import HttpMessageApiBase, HttpBase


@dataclass
class TelegramMessage(HttpMessageApiBase):
    """:class:`TelegramMessage` instance created by :class:`Telegram` component. Create It using::

        from then.components import Telegram

        message = Telegram(...).message(body="My message")
        message.send()

    :arg body: message to send.
    """
    body: str
    component: 'Telegram' = None
    url_pattern = 'https://api.telegram.org/bot{component.token}/{component.send_method}'

    def get_body(self):
        return {
            'chat_id': self.component.to,
            'text': self.body
        }


@dataclass
class Telegram(HttpBase):
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
    send_method: str = 'sendMessage'
    timeout: int = 15
    method: str = 'POST'

    _message_class = TelegramMessage
