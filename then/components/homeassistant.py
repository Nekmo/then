from dataclasses import dataclass

from then.components.http import Http, HttpMessageOwnApiBase


class HomeAssistantMessage(HttpMessageOwnApiBase):

    def __init__(self, event: str, default_port: int = 8123, component: 'HomeAssistant' = None):
        self.event = event
        self.default_port = default_port
        self.component = component
        self.__post_init__()

    def get_url(self):
        """Home assistant url

        :return: url
        :rtype: str
        """
        url = super().get_url()
        url += '/api/events/{}'.format(self.event)
        return url


@dataclass
class HomeAssistant(Http):
    method: str = 'post'
    access: str = None
    timeout: int = 15
    _message_class = HomeAssistantMessage

    def get_headers(self):
        return {
            'x-ha-access': self.access
        } if self.access else {}
