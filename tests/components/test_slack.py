import unittest
import urllib.parse

from tests.components.http_base import TestHttpMessageApiMixIn
from then.components.http import CONTENT_TYPE_ALIASES
from then.components.slack import Slack, SlackMessage


class TestSlack(TestHttpMessageApiMixIn, unittest.TestCase):
    team = 'T00000000'
    bot = 'B00000000'
    token = 'XXXXXXXXXXXXXXXXXXXXXXXX'
    body = 'foo'

    def get_component(self, **kwargs):
        return Slack(self.team, self.bot, self.token, **kwargs)

    def test_send(self):
        slack = self.get_component()
        message = slack.message(body=self.body)
        req_text = 'payload={}'.format(urllib.parse.quote(message.get_body()['payload'])).replace('%20', '+')
        self.session_mock.post(SlackMessage.url_pattern.format(component=self),
                               request_headers={'Content-Type': CONTENT_TYPE_ALIASES['form']},
                               additional_matcher=lambda req: req.text == req_text)
        message.send()

    def test_payload_text(self):
        then = self.get_component()
        self.assertEqual(then.message(body=self.body).get_payload(), {
            'text': self.body, 'icon_emoji': then.icon, 'username': then.from_,
        })

    def test_payload_icon_emoji(self):
        icon = ':foo:'
        then = self.get_component(icon=icon)
        self.assertEqual(then.message(body=self.body).get_payload().get('icon_emoji'), icon)

    def test_payload_icon_url(self):
        icon = 'http://path.to/image.jpg'
        then = self.get_component(icon=icon)
        self.assertEqual(then.message(body=self.body).get_payload().get('icon_url'), icon)
