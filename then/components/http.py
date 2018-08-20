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


class HttpException(ExecuteError):
    def __init__(self, response):
        message = '"{}" return code {}.\n{}'.format(response.request.url, response.status_code, response.text)
        super().__init__(message)
        self.response = response


class HttpMessageBase(Message):
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
                self._body = json.dumps(self._body)
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
                           auth=self.component.get_auth(),
                           headers=headers)
        except RequestException as e:
            raise ExecuteError('Exception on request to {}: {}'.format(url, e))
        if resp.status_code >= 400:
            raise HttpException(resp)

        data = resp.raw.read(self.component.max_body_read, decode_content=True)
        data = data.decode('utf-8', errors='ignore')
        return data


@dataclass
class HttpMessage(HttpMessageBase):
    """:class:`HttpMessage` instance created by :class:`Http` component. Create It using::

        from then.components import Http

        message = Http(...).message(body={"username": "foo"},
                                    content_type="form")
        message.send()

    :param body: Request payload. Only if the method is ``POST``/``PUT``/``PATCH``.
    """
    body: Union[str, dict] = None
    component: 'Http' = None



class HttpBase(Component):
    url: str = None
    method: str = 'get'
    headers: {} = None
    content_type: str = None
    auth: str = None
    max_body_read: int = 102400
    timeout: int = 15

    _message_class = None

    def __post_init__(self):
        self.method = self.method.lower()
        if self.method not in METHODS:
            raise ValidationError('Error on {}: {} is not a valid method. Valid methods: {}'.format(
                self.name, self.method, ', '.join(METHODS)
            ))
        self.content_type = CONTENT_TYPE_ALIASES.get(self.content_type, self.content_type)

    def get_headers(self):
        return dict(self.headers or {})

    def get_auth(self):
        return tuple(self.auth.split(':', 1)) if self.auth else None


@dataclass
class Http(HttpBase):
    """Create a Http instance to send a message to a user or channel::

        from then.components import Http

        Http(url="http://some-address/api/")\\
            .send(body={"option": "bar"})

    :param url: Home Assistant address. Syntax: ``<protocol>://<server>[:<port>]``.
    :param headers: Headers to send to the server. ``content_type`` will be overwritten if it is defined later.
    :param content_type: HTTP Content-Type Header on request. For example: ``text/plain``.
    :param auth: HTTP Basic Auth. Syntax: ``<user>:<password>``.
    :param max_body_read: Maximum size to read from the server.
    :param timeout: Connection timeout to send message.
    """
    url: str
    method: str = 'get'
    headers: {} = None
    content_type: str = None
    timeout: int = 15
    auth: str = None
    max_body_read: int = 102400

    _message_class = HttpMessage


class HttpMessageApiBase(HttpMessageBase):
    url_pattern: str = None

    def get_url(self):
        url = self.url_pattern.format(**vars(self))
        return url


class HttpMessageOwnApiBase(HttpMessageBase):
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
