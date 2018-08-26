from dataclasses import dataclass

from then.components.http import HttpBase, HttpMessageApiBase


@dataclass
class HangoutsMessage(HttpMessageApiBase):
    """:class:`HangoutsMessage` instance created by :class:`Hangouts` component. Create It using::

        from then.components import Hangouts

        message = Hangouts(...).message(body="My message")
        message.send()

    :arg body: message to send.
    """
    body: str
    url_pattern = 'https://chat.googleapis.com/v1/spaces/{component.to}/' \
                  'messages?key={component.key}&token={component.token}'
    component: 'Hangouts' = None

    def get_body(self):
        return {
            'text': self.body,
        }


@dataclass
class Hangouts(HttpBase):
    """Create a Hangouts instance to send a message to a group::

        from then.components import Hangouts

        Hangouts(account='AIzaSfDdI7hChtE6zyS6Mm-WefRa3Cpzqlqxxxx',
                 token='IWccInfAQhPSrkOVgVSzh07W9hBzp9eCqjQzTB_xxxxxxx',
                 to='AAAAqkJxxxx')\\
            .send(body='My message')

    :param key: Hangouts Chat Webhook key.
    :param token: Hangouts Chat Webhook token.
    :param to: Space ID
    """
    key: str
    token: str
    to: str
    timeout: int = 15
    method = 'POST'

    _message_class = HangoutsMessage
