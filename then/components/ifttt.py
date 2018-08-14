from dataclasses import dataclass

from then.components.http import Http, HttpMessageApiBase


@dataclass
class IftttMessage(HttpMessageApiBase):
    event: str
    url_pattern = 'https://maker.ifttt.com/trigger/{event}/with/key/{component.key}'
    component: 'Ifttt' = None


@dataclass
class Ifttt(Http):
    key: str
    timeout: int = 15
