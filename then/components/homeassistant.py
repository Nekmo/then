from dataclasses import dataclass

from then.components.http import Http, HttpMessageOwnApiBase


@dataclass
class HomeAssistantMessage(HttpMessageOwnApiBase):
    event: str
    default_port: str = 8123
    component: 'HomeAssistant' = None

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
    access: str = None
    timeout: int = 15

    def get_headers(self):
        return {
            'x-ha-access': self.access
        } if self.access else {}
