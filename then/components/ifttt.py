from dataclasses import dataclass

from then.components.http import HttpBase, HttpMessageApiBase


@dataclass
class IftttMessage(HttpMessageApiBase):
    """:class:`IftttMessage` instance created by :class:`Ifttt` component. Create It using::

        from then.components import Ifttt

        message = Ifttt(...).message(event='otherevent')
        message.send()

    :arg event: You define the event name when creating a Webhook applet.
    """
    event: str
    url_pattern = 'https://maker.ifttt.com/trigger/{event}/with/key/{component.key}'
    component: 'Ifttt' = None

    def get_body(self):
        return self.extra

    def send(self):
        self._body = self.update_body(self.get_body())
        super().send()


@dataclass
class Ifttt(HttpBase):
    """Create a Ifttt instance to send a message to a user or channel::

        from then.components import Ifttt

        Ifttt(token="c2BVn_A93kLvaa4ymExxxx")\\
            .send(event='myevent', ingredient1='foo')

    :param token: Get your token here: https://ifttt.com/services/maker_webhooks/settings
    :param timeout: Connection timeout to send message.
    """
    key: str
    method = 'post'
    timeout: int = 15

    _message_class = IftttMessage
