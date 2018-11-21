from dataclasses import dataclass

from then.components.http import HttpBase, HttpMessageApiBase


@dataclass
class GoogleChatMessage(HttpMessageApiBase):
    """:class:`GoogleChatMessage` instance created by :class:`GoogleChat` component. Create It using::

        from then.components import GoogleChat

        message = GoogleChat(...).message(body="My message")
        message.send()

    :arg body: message to send.
    """
    body: str
    url_pattern = 'https://chat.googleapis.com/v1/spaces/{component.to}/' \
                  'messages?key={component.key}&token={component.token}'
    component: 'GoogleChat' = None

    def get_body(self):
        return {
            'text': self.body,
        }


@dataclass
class GoogleChat(HttpBase):
    """Create a GoogleChat instance to send a message to a group::

        from then.components import GoogleChat

        GoogleChat(key='AIzaSfDdI7hChtE6zyS6Mm-WefRa3Cpzqlqxxxx',
                 token='IWccInfAQhPSrkOVgVSzh07W9hBzp9eCqjQzTB_xxxxxxx',
                 to='AAAAqkJxxxx')\\
            .send(body='My message')

    :param key: GoogleChat Webhook key.
    :param token: GoogleChat Webhook token.
    :param to: Space ID
    """
    key: str
    token: str
    to: str
    timeout: int = 15
    method = 'POST'

    _message_class = GoogleChatMessage
    _type = 'message'
