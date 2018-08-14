from dataclasses import dataclass

from then.components.http import Http, HttpMessageOwnApiBase


@dataclass
class OpenHabMessage(HttpMessageOwnApiBase):
    item: str
    state: str = 'ON'
    default_port: int = 8080
    component: 'OpenHab' = None

    def get_url(self):
        """Open Hab url

        :return: url
        :rtype: str
        """
        url = super().get_url()
        url += '/rest/items/{}'.format(self.item)
        return url

    def get_body(self):
        return self.state


@dataclass
class OpenHab(Http):
    url: str
    method: str = 'post'
    access: str = None
    timeout: int = 15
    content_type: str = 'text/plain'

    def get_headers(self):
        return dict(Accept='application/json', **{
            'x-ha-access': self.access
        } if self.access else {})
