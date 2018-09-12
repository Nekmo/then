import unittest

from tests.components.http_base import TestHttpMessageApiMixIn
from then.components.http import CONTENT_TYPE_ALIASES
from then.components.line import Line, LineMessage
from then.exceptions import ValidationError


class TestLine(TestHttpMessageApiMixIn, unittest.TestCase):
    token = 'iJGhOHToGD5jCvawpigcKB7qpYAK6WRXTMWZYR3xxxx'
    body = 'foo'

    def get_component(self, **kwargs):
        return Line(self.token, **kwargs)

    def test_send(self):
        line = self.get_component()
        message: LineMessage = line.message(body=self.body)
        self.session_mock.post(LineMessage.url_pattern,
                               request_headers={'Content-Type': CONTENT_TYPE_ALIASES['form']},
                               additional_matcher=lambda req: req.text == 'message=foo'
                               )
        message.send()

    def test_invalid_sticker_usage(self):
        with self.assertRaises(ValidationError):
            LineMessage('foo', 100)
        with self.assertRaises(ValidationError):
            LineMessage('foo', 0, 45)
