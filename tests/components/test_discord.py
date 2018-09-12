import json
import unittest
from unittest.mock import Mock, MagicMock, patch

from tests.components.http_base import TestHttpMessageApiMixIn
from then.components import Discord, DiscordMessage
from then.components.http import CONTENT_TYPE_ALIASES
from then.exceptions import ValidationError, ExecuteError


class TestDiscord(TestHttpMessageApiMixIn, unittest.TestCase):
    token = 'NDF4NGQ5GzY6OTF3MAk2vDc1.D1xvWv.nMarFQh3UdjaDLXZZggL1xxxxxx'
    to = '48014601482xxxx01'
    body = 'My message body'

    def get_component(self, **kwargs):
        return Discord(self.token, self.to, **kwargs)

    def test_send_without_login(self):
        discord = self.get_component()
        message = discord.message(body=self.body)
        req_text = json.dumps({"content": self.body})
        self.session_mock.post(message.get_url(),
                               request_headers={'Content-Type': CONTENT_TYPE_ALIASES['json']},
                               additional_matcher=lambda req: req.text == req_text)
        message.send()

    def test_send_login_required(self):
        discord = self.get_component()
        message = discord.message(body=self.body)
        m1 = self.session_mock.post(message.get_url(), [dict(status_code=400), dict(status_code=200)])
        m2 = self.session_mock.get(message.url_pattern.format('users/@me'))
        message.connect = Mock()
        message.send()
        message.connect.assert_called_once()
        self.assertTrue(m1.call_count, 2)
        self.assertTrue(m2.called_once)

    @patch.object(DiscordMessage, 'create_gateway')
    @patch.object(DiscordMessage, 'gateway_send')
    def test_connect(self, m1, m2):
        self.get_component().message().connect()
        m1.assert_called_once()
        m2.assert_called_once()

    def test_login_error(self):
        message = self.get_component().message()
        self.session_mock.get(message.url_pattern.format('users/@me'), status_code=401)
        with self.assertRaises(ValidationError):
            self.get_component().message().login()

    def test_login_unknown_error(self):
        message = self.get_component().message()
        self.session_mock.get(message.url_pattern.format('users/@me'), status_code=400)
        with self.assertRaises(ExecuteError):
            self.get_component().message().login()
