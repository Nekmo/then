from urllib.parse import unquote

import requests_mock


def form_to_dict(data):
    items = [item.split('=') for item in data.split('&')]
    return {unquote(item[0]): unquote(item[1]) for item in items}


class TestHttpMessageApiMixIn:
    url = ''
    method = 'get'

    def get_component(self):
        raise NotImplementedError

    def setUp(self):
        super().setUp()
        self.session_mock = requests_mock.Mocker()
        self.session_mock.start()

    def tearDown(self):
        super().tearDown()
        self.session_mock.stop()
