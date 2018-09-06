import base64
import json
import unittest

import requests
import requests_mock
from requests_mock import NoMockAddress

from then.components.http import Http
from then.exceptions import ValidationError, ExecuteError


class TestHttp(unittest.TestCase):
    no_body_methods = ['get', 'head', 'delete', 'connect', 'options', 'trace']
    url = 'http://domain.com'

    def setUp(self):
        super(TestExecuteUrl, self).setUp()
        self.session_mock = requests_mock.Mocker()
        self.session_mock.start()
        self.get_mock = self.session_mock.get(self.url)
        pass

    def test_invalid_method(self):
        with self.assertRaises(ValidationError):
            Http(self.url, method='spam').message()

    def test_content_type_invalid_method(self):
        for method in self.no_body_methods:
            with self.assertRaises(ValidationError):
                Http(self.url, method=method, content_type='form').send()

    def test_body_invalid_method(self):
        for method in self.no_body_methods:
            with self.assertRaises(ValidationError):
                Http(self.url, method=method).send(body='spam')

    def test_json_data(self):
        data = {'foo': 'bar'}
        message = Http(self.url, method='post').message(body=data)
        self.assertEqual(message._body, json.dumps(data))
        self.assertEqual(message.content_type, 'application/json')

    def test_invalid_json_data(self):
        with self.assertRaises(ValidationError):
            Http(self.url, method='post').message(body={'foo': lambda x: x})

    def test_form_invalid_data(self):
        with self.assertRaises(ValidationError):
            Http(self.url, method='post', content_type='form').message(body='inval')

    def test_dict_invalid_content_type(self):
        with self.assertRaises(ValidationError):
            Http(self.url, method='post', content_type='plain').message(body={'foo': 3})

    def test_send(self):
        Http(self.url).send()
        self.assertTrue(self.get_mock.called_once)

    def test_execute_headers(self):
        self.session_mock.post(self.url, request_headers={'authorization': 'foo'})
        Http(self.url, method='post', headers={'authorization': 'foo'}).send()
        self.assertEqual(self.session_mock.call_count, 1)

        with self.assertRaises(NoMockAddress):
            Http(self.url, method='post', headers={'authorization': 'bar'}).send()

    def test_execute_content_type(self):
        self.session_mock.post(self.url, request_headers={'content-type': 'foo'})
        Http(self.url, method='post', content_type='foo').send()
        self.assertEqual(self.session_mock.call_count, 1)

        with self.assertRaises(NoMockAddress):
            Http(self.url, method='post', content_type='bar').send()

    def test_execute_body(self):
        self.session_mock.post(self.url, additional_matcher=lambda r: r.body == 'foo')
        Http(self.url, method='post').send(body='foo')
        self.assertEqual(self.session_mock.call_count, 1)

        with self.assertRaises(NoMockAddress):
            Http(self.url, method='post').send(body='bar')

    def test_execute_exception(self):
        self.session_mock.post(self.url, exc=requests.exceptions.ConnectTimeout)
        with self.assertRaises(ExecuteError):
            Http(self.url, method='post').send()

    def test_execute_400(self):
        self.session_mock.post(self.url, status_code=400)
        with self.assertRaises(ExecuteError):
            Http(self.url, method='post').send()

    def test_authorization(self):
        auth = b'Basic ' + base64.b64encode(b'foo:bar')
        auth = auth.decode('utf-8')
        self.session_mock.post(self.url, request_headers={'Authorization': auth})
        Http(self.url, method='post', auth='foo:bar').send()

    def tearDown(self):
        super(TestExecuteUrl, self).tearDown()
        self.session_mock.stop()
