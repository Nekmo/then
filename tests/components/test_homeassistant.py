import unittest

from tests.components.http_base import TestHttpMessageApiMixIn
from then.components.homeassistant import HomeAssistant, HomeAssistantMessage


class TestHomeAssistant(TestHttpMessageApiMixIn, unittest.TestCase):
    url = 'http://localhost:3128'
    event = 'foo'
    access = 'bar'

    def get_component(self, **kwargs):
        return HomeAssistant(self.url, **kwargs)

    def test_send(self):
        homeassistant = self.get_component()
        message: HomeAssistantMessage = homeassistant.message(event=self.event)
        self.assertIn(self.event, message.get_url())
        self.session_mock.post(message.get_url())
        message.send()

    def test_access(self):
        homeassistant = self.get_component(access=self.access)
        message: HomeAssistantMessage = homeassistant.message(event=self.event)
        self.session_mock.post(message.get_url(), headers={'x-ha-access': self.access})
        message.send()
