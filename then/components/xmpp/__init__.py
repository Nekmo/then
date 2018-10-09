from __future__ import absolute_import

from dataclasses import dataclass

from then.components.base import Component, Message, split_host_port
from then.exceptions import ExecuteError


GOOGLE_SERVER = ('talk.google.com', 5222)


@dataclass
class XmppMessage(Message):
    """:class:`XmppMessage` instance created by :class:`Xmpp` component. Create It using::

        from then.components import Xmpp

        message = Xmpp(...).message(body="My message")
        message.send()

    :arg body: message to send.
    """
    body: str
    component: 'Xmpp' = None

    def send(self):
        from then.components.xmpp.send_msg import SendMsgBot
        xmpp = SendMsgBot(self.component.from_,
                          self.component.password,
                          self.component.to,
                          self.body)
        xmpp.register_plugin('xep_0030')  # Service Discovery
        xmpp.register_plugin('xep_0199')  # XMPP Ping
        if self.component.server:
            server = split_host_port(self.component.server, 5222)
        elif self.component.from_.endswith('@gmail.com'):
            server = GOOGLE_SERVER
        else:
            server = ()
        if xmpp.connect(server):
            # If you do not have the dnspython library installed, you will need
            # to manually specify the name of the server if it does not match
            # the one in the JID. For example, to use Google Talk you would
            # need to use:
            #
            # if xmpp.connect(('talk.google.com', 5222)):
            #     ...
            xmpp.process(block=True)
        else:
            raise ExecuteError('Unable to connect.')


@dataclass
class Xmpp(Component):
    """Create a Xmpp instance to send a message to a user::

        from then.components import Xmpp

        Xmpp(from_='account1@gmail.com', password='mypass',
             to='account2@gmail.com')\\
            .send(body='Message to group')

    :param from_: Jabber ID Account (JID).
    :param password: Password for from_ account.
    :param to: destination JID.
    :param server: server for from_ account.
    """
    from_: str
    password: str
    to: str
    server: str = None

    _message_class = XmppMessage
