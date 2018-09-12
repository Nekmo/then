from dataclasses import dataclass

from then.components.http import HttpBase, HttpMessageApiBase
from then.exceptions import ValidationError


@dataclass
class LineMessage(HttpMessageApiBase):
    """:class:`LineMessage` instance created by :class:`Line` component. Create It using::

        from then.components import Line

        message = Line(...).message(body="My message", sticker_id=283, package_id=4)
        message.send()

    :arg body: message to send.
    :arg sticker_id: sticker to send. package_id is required.
    :arg package_id: message to send. sticker_id is required.
    """
    body: str
    sticker_id: int = None
    package_id: int = None
    url_pattern = 'https://notify-api.line.me/api/notify'
    component: 'Line' = None

    def __post_init__(self):
        if (self.sticker_id and not self.package_id) or (not self.sticker_id and self.package_id):
            raise ValidationError('A sticker_id and a package_id are required for send a sticker.')
        super().__post_init__()

    def get_body(self):
        body = {
            'message': self.body,
            'stickerId': self.sticker_id,
            'stickerPackageId': self.package_id,
        }
        return {key: value for key, value in body.items() if value is not None}


@dataclass
class Line(HttpBase):
    """Create a Line instance to send a message to a user or group::

        from then.components import Line

        Line(token='iJGhOHToGD5jCvawpigcKB7qpYAK6WRXTMWZYR3xxxx')\\
            .send(body='My message body')

    :param token: LINE Notify token
    :param timeout: Connection timeout to send message.
    """
    token: str
    timeout: int = 15
    content_type = 'form'
    method = 'POST'

    _message_class = LineMessage

    def get_headers(self):
        return {
            'Authorization': 'Bearer {}'.format(self.token),
        }
