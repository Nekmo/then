import unittest

from tests.components.http_base import TestHttpMessageApiMixIn
from then.components.http import CONTENT_TYPE_ALIASES
from then.components.openhab import OpenHab, OpenHabMessage


class TestOpenHab(TestHttpMessageApiMixIn, unittest.TestCase):
    url = 'http://localhost:3128'
    item = 'foo'

    def get_component(self, **kwargs):
        return OpenHab(self.url, **kwargs)

    def test_send(self):
        openhab = self.get_component()
        message: OpenHabMessage = openhab.message(item=self.item)
        self.assertIn(self.item, message.get_url())
        self.session_mock.post(message.get_url(),
                               request_headers={'Content-Type': CONTENT_TYPE_ALIASES['plain']},
                               additional_matcher=lambda req: req.text == 'ON')
        message.send()
