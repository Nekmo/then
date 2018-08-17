from dataclasses import dataclass

from then.components.http import HttpBase, HttpMessageApiBase


@dataclass
class IftttMessage(HttpMessageApiBase):
    event: str
    url_pattern = 'https://maker.ifttt.com/trigger/{event}/with/key/{component.key}'
    component: 'Ifttt' = None


@dataclass
class Ifttt(HttpBase):
    key: str
    timeout: int = 15

    _message_class = IftttMessage
