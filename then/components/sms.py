from dataclasses import dataclass

from then.components.http import HttpBase, HttpMessageApiBase


@dataclass
class SmsMessage(HttpMessageApiBase):
    """:class:`SmsMessage` instance created by :class:`Sms` component. Create It using::

        from then.components import Sms

        message = Sms(...).message(body="My message")
        message.send()

    :arg body: message to send.
    """
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
    """Create a Sms instance to send a message to a phone::

        from then.components import Sms

        Sms(account='AC3z4xabc4867ddc2441acda6b1834xxxx',
            token='bcc8476384cc714h991dc56d1906xxxx',
            from_='+34612345678',
            to='+34687654321')\\
            .send(body='My message')

    :param account: Twilio account.
    :param token: Secret Auth Token.
    :param from_: Twilio phone.
    :param to: Receipt phone.
    """
    account: str
    token: str
    from_: str
    to: str
    timeout: int = 15
    content_type = 'form'
    method = 'POST'

    _message_class = SmsMessage
    _type = 'message'

    def get_auth(self):
        return (self.account, self.token)
