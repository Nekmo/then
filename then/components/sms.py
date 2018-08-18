from dataclasses import dataclass

from then.components.http import HttpBase, HttpMessageApiBase

# https://www.twilio.com/console/sms/getting-started/build

@dataclass
class SmsMessage(HttpMessageApiBase):
    body: str
    url_pattern = 'https://api.twilio.com/2010-04-01/Accounts/{component.account}/Messages.json'
    component: 'Sms' = None

    def get_body(self):
        return {
            'From': self.component.from_,
            'To': self.component.to,
            'Body': self.body,
        }


@dataclass
class Sms(HttpBase):
    account: str
    token: str
    from_: str
    to: str
    timeout: int = 15
    content_type = 'form'
    method = 'POST'

    _message_class = SmsMessage

    def get_auth(self):
        return (self.account, self.token)
