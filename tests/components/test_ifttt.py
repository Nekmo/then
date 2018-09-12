import unittest

from tests.components.http_base import TestHttpMessageApiMixIn
from then.components.http import CONTENT_TYPE_ALIASES
from then.components.ifttt import Ifttt, IftttMessage
from then.exceptions import ValidationError


class TestIfttt(TestHttpMessageApiMixIn, unittest.TestCase):
    key = 'iJGhOHToGD5jCvawpigcKB7qpYAK6WRXTMWZYR3xxxx'
    event = 'foo'

    def get_component(self, **kwargs):
        return Ifttt(self.key, **kwargs)

    def test_send(self):
        ifttt = self.get_component()
        message: IftttMessage = ifttt.message(event=self.event)
        self.session_mock.get(IftttMessage.url_pattern.format(event=self.event, component=ifttt))
        message.send()
