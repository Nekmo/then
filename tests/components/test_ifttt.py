import json
import unittest

from tests.components.http_base import TestHttpMessageApiMixIn
from then.components.http import CONTENT_TYPE_ALIASES
from then.components.ifttt import Ifttt, IftttMessage


class TestIfttt(TestHttpMessageApiMixIn, unittest.TestCase):
    key = 'iJGhOHToGD5jCvawpigcKB7qpYAK6WRXTMWZYR3xxxx'
    event = 'foo'

    def get_component(self, **kwargs):
        return Ifttt(self.key, **kwargs)

    def test_send(self):
        ifttt = self.get_component()
        message: IftttMessage = ifttt.message(event=self.event)
        self.session_mock.post(IftttMessage.url_pattern.format(event=self.event, component=ifttt))
        message.send()

    def test_send_ingredients(self):
        ifttt = self.get_component()
        body = dict(value1='foo')
        message: IftttMessage = ifttt.message(event=self.event, **body)
        req_text = json.dumps(body)
        self.session_mock.post(IftttMessage.url_pattern.format(event=self.event, component=ifttt),
                               request_headers={'Content-Type': CONTENT_TYPE_ALIASES['json']},
                               additional_matcher=lambda req: req.text == req_text                               )
        message.send()
