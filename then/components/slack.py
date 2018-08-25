import json

from dataclasses import dataclass

from then.components.http import HttpBase, HttpMessageApiBase

# Get your Webhook url here:
# https://slack.com/apps/A0F7XDUAZ-incoming-webhooks
# For example:
# https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX
#
# Parameters:
# Team (first param, starts with T)
# Bot (second param, starts with B)
# Token (third param)


@dataclass
class SlackMessage(HttpMessageApiBase):
    """:class:`SlackMessage` instance created by :class:`Slack` component. Create It using::

        from then.components import Slack

        message = Slack(...).message(body="My message")
        message.send()

    :arg body: message to send.
    """
    body: str
    url_pattern = 'https://hooks.slack.com/services/{component.team}/{component.bot}/{component.token}'
    component: 'Slack' = None

    def get_body(self):
        return {
            'payload': json.dumps({key: value for key, value
                                   in self.get_payload().items() if value is not None}),
        }
    def get_payload(self):
        payload = {
            'text': self.body,
            'channel': self.component.to,
            'username': self.component.from_
        }
        payload = {key: value for key, value in payload.items() if value is not None}
        if self.component.icon:
            icon = self.component.icon
            payload['icon_emoji' if icon.startswith(':') and icon.endswith(':') else 'icon_url'] = icon
        return payload


@dataclass
class Slack(HttpBase):
    """Create a Slack instance to send a message to a user or channel::

        from then.components import Slack

        Slack(team='T00000000', bot='B00000000', token='XXXXXXXXXXXXXXXXXXXXXXXX')\\
            .send(body='My message body')

    :param team: First param from Webhook
    :param bot: Second param from Webhook
    :param token: Third param from Webhook
    :param from_: Bot username
    :param to: Channel (``#other-channel``) or user (``@username``)
    :param icon: Image URL or emoticon. By default *:robot_face:*.
    :param timeout: Connection timeout to send message.
    """
    team: str
    bot: str
    token: str
    from_: str = 'THEN'
    to: str = None
    icon: str = ':robot_face:'
    timeout: int = 15
    content_type = 'form'
    method = 'POST'

    _message_class = SlackMessage
