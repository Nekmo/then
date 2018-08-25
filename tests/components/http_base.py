import requests_mock


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
