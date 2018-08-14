import json
from json import JSONDecodeError
from typing import Union

from dataclasses import dataclass
from requests import request, RequestException

from then.components.base import Component, Message
from then.exceptions import ValidationError, ExecuteError

METHODS = [
    'get',
    'head',
    'post',
    'put',
    'delete',
    'connect',
    'options',
    'trace',
    'patch'
]
CONTENT_TYPE_METHODS = ['post', 'put', 'patch']
CONTENT_TYPE_ALIASES = {
    'form': 'application/x-www-form-urlencoded',
    'json': 'application/json',
    'plain': 'text/plain',
}


@dataclass
class HttpMessage(Message):
    body: Union[str, dict] = None
    component: 'Http' = None

    def __post_init__(self):
        self.url = self.component.url
        self.content_type = self.component.content_type
        if (self.content_type or self.body) and self.component.method not in CONTENT_TYPE_METHODS:
            raise ValidationError(
                'Error on {}: The body/content-type option only can be used with the {} methods.'.format(
                    self.component.name, ', '.join(CONTENT_TYPE_METHODS)
                ))
        if isinstance(self.body, dict) and (self.content_type == CONTENT_TYPE_ALIASES['json'] or not self.content_type):
            self.content_type = CONTENT_TYPE_ALIASES['json']
            try:
                self.body = json.loads(self.body)
            except JSONDecodeError:
                raise ValidationError(
                    'Error on {}: Invalid JSON body: {}'.format(self.component.name, self.body)
                )
        if isinstance(self.body, dict) and self.content_type != CONTENT_TYPE_ALIASES['form']:
            raise ValidationError(
                'Error on {}: invalid content-type for {} (dict data type)'.format(
                    self.component.name, self.body)
            )

    def send(self):
        headers = self.component.get_headers()
        if self.content_type:
            headers['content-type'] = self.content_type or headers.get('content-type') or None
        try:
            resp = request(self.component.method, self.url, data=self.body, timeout=self.component.timeout,
                           stream=True, auth=tuple(self.component.auth.split(':', 1)), headers=headers)
        except RequestException as e:
            raise ExecuteError('Exception on request to {}: {}'.format(self.url, e))
        if resp.status_code >= 400:
            raise ExecuteError('"{}" return code {}.'.format(self.url, resp.status_code))
        data = resp.raw.read(self.component.max_body_read, decode_content=True)
        data = data.decode('utf-8', errors='ignore')
        return data


@dataclass
class Http(Component):
    url: str
    method: str = 'get'
    headers: {} = None
    content_type: str = None
    timeout: int = 15
    auth: str = None
    max_body_read: int = 10000

    def __post_init__(self):
        self.method = self.method.lower()
        if self.method not in METHODS:
            raise ValidationError('Error on {}: {} is not a valid method. Valid methods: {}'.format(
                self.name, self.method, ', '.join(METHODS)
            ))
        self.content_type = CONTENT_TYPE_ALIASES.get(self.content_type, self.content_type)

    def get_headers(self):
        return dict(self.headers or {})
