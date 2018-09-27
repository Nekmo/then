import json
import unittest

from tests.components.http_base import TestHttpMessageApiMixIn, form_to_dict
from then.components.http import CONTENT_TYPE_ALIASES
from then.components.sms import Sms, SmsMessage


class TestSms(TestHttpMessageApiMixIn, unittest.TestCase):
    account = 'AC3z4xabc4867ddc2441acda6b1834xxxx'
    token = 'bcc8476384cc714h991dc56d1906xxxx'
    from_ = '+34612345678'
    to = '+34687654321'
    body = 'foo'

    def get_component(self, **kwargs):
        return Sms(self.account, self.token, self.from_, self.to, **kwargs)

    def test_send(self):
        sms = self.get_component()
        message: SmsMessage = sms.message(body=self.body)
        self.session_mock.post(SmsMessage.url_pattern.format(component=sms),
                               request_headers={'Content-Type': CONTENT_TYPE_ALIASES['form']},
                               additional_matcher=lambda x: form_to_dict(x.text) == message.get_body())
        message.send()

    def test_get_body(self):
        sms = self.get_component()
        self.assertEqual(sms.message(body=self.body).get_body(), {'Body': self.body, 'From': self.from_,
                                                                  'To': self.to})

    def test_get_auth(self):
        sms = self.get_component()
        self.assertEqual(sms.get_auth(), (self.account, self.token))
