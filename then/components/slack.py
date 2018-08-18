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
        if self.component.icon:
            icon = self.component.icon
            payload['icon_emoji' if icon.startswith(':') and icon.endswith(':') else 'icon_url'] = icon
        return payload


@dataclass
class Slack(HttpBase):
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
