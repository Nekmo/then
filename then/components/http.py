from __future__ import absolute_import
import json
from json import JSONDecodeError
from typing import Union
from urllib.parse import urlparse

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
        self._body = self.get_body()
        self.content_type = self.component.content_type
        if (self.content_type or self._body) and self.component.method not in CONTENT_TYPE_METHODS:
            raise ValidationError(
                'Error on {}: The body/content-type option only can be used with the {} methods.'.format(
                    self.component.name, ', '.join(CONTENT_TYPE_METHODS)
                ))
        if isinstance(self._body, dict) and (self.content_type == CONTENT_TYPE_ALIASES['json'] or
                                             not self.content_type):
            self.content_type = CONTENT_TYPE_ALIASES['json']
            try:
                self._body = json.loads(self._body)
            except JSONDecodeError:
                raise ValidationError(
                    'Error on {}: Invalid JSON body: {}'.format(self.component.name, self._body)
                )
        if isinstance(self._body, dict) and self.content_type != CONTENT_TYPE_ALIASES['form']:
            raise ValidationError(
                'Error on {}: invalid content-type for {} (dict data type)'.format(
                    self.component.name, self._body)
            )

    def get_url(self):
        return self.component.url

    def get_body(self):
        return self.body

    def send(self):
        headers = self.component.get_headers()
        url = self.get_url()
        if self.content_type:
            headers['content-type'] = self.content_type or headers.get('content-type') or None
        try:
            resp = request(self.component.method, url, data=self._body, timeout=self.component.timeout, stream=True,
                           auth=tuple(self.component.auth.split(':', 1)) if self.component.auth else None,
                           headers=headers)
        except RequestException as e:
            raise ExecuteError('Exception on request to {}: {}'.format(url, e))
        if resp.status_code >= 400:
            raise ExecuteError('"{}" return code {}.'.format(url, resp.status_code))
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

    _message_class = HttpMessage

    def __post_init__(self):
        self.method = self.method.lower()
        if self.method not in METHODS:
            raise ValidationError('Error on {}: {} is not a valid method. Valid methods: {}'.format(
                self.name, self.method, ', '.join(METHODS)
            ))
        self.content_type = CONTENT_TYPE_ALIASES.get(self.content_type, self.content_type)

    def get_headers(self):
        return dict(self.headers or {})


class HttpMessageApiBase(HttpMessage):
    url_pattern: str = None

    def get_url(self):
        url = self.url_pattern.format(**vars(self))
        return url


class HttpMessageOwnApiBase(HttpMessage):
    default_protocol: str = 'http'
    default_port: int = 0
    component: Http = None

    def get_url(self):
        """API url

        :return: url
        :rtype: str
        """
        url = self.component.url
        parsed = urlparse(url)
        if not parsed.scheme:
            url = '{}://{}'.format(self.default_protocol, url)
        if not url.split(':')[-1].isalnum():
            url += ':{}'.format(self.default_port)
        return url
