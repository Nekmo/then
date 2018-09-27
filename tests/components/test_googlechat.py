import json
import unittest

from tests.components.http_base import TestHttpMessageApiMixIn
from then.components.http import CONTENT_TYPE_ALIASES
from then.components.googlechat import GoogleChat, GoogleChatMessage


class TestGoogleChat(TestHttpMessageApiMixIn, unittest.TestCase):
    key = 'AIzaSfDdI7hChtE6zyS6Mm-WefRa3Cpzqlqxxxx'
    token = 'IWccInfAQhPSrkOVgVSzh07W9hBzp9eCqjQzTB_xxxxxxx'
    to = 'AAAAqkJxxxx'
    body = 'foo'

    def get_component(self, **kwargs):
        return GoogleChat(self.key, self.token, self.to, **kwargs)

    def test_send(self):
        google_chat = self.get_component()
        message: GoogleChatMessage = google_chat.message(body=self.body)
        req_text = json.dumps(message.get_body())
        self.session_mock.post(GoogleChatMessage.url_pattern.format(component=self),
                               request_headers={'Content-Type': CONTENT_TYPE_ALIASES['json']},
                               additional_matcher=lambda req: req.text == req_text)
        message.send()

    def test_get_body(self):
        then = self.get_component()
        self.assertEqual(then.message(body=self.body).get_body(), {'text': self.body})
