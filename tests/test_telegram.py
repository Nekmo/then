import json
import unittest

from tests.components.http_base import TestHttpMessageApiMixIn
from then.components.http import CONTENT_TYPE_ALIASES
from then.components.telegram import Telegram, TelegramMessage


class TestTelegram(TestHttpMessageApiMixIn, unittest.TestCase):
    token = '520604247:ABF0EHnzZxDIQ15Re83iWZojuvja24Exxxx'
    to = '-600503825xxxx'
    body = 'foo'

    def get_component(self, **kwargs):
        return Telegram(self.token, self.to, **kwargs)

    def test_send(self):
        telegram = self.get_component()
        message: TelegramMessage = telegram.message(body=self.body)
        self.session_mock.post(TelegramMessage.url_pattern.format(component=telegram),
                               request_headers={'Content-Type': CONTENT_TYPE_ALIASES['json']},
                               additional_matcher=lambda x: json.loads(x.text) == message.get_body())
        message.send()

    def test_get_body(self):
        telegram = self.get_component()
        self.assertEqual(telegram.message(body=self.body).get_body(), {'chat_id': self.to, 'text': self.body})
