from __future__ import absolute_import

import sleekxmpp as sleekxmpp
from dataclasses import dataclass

from then.components.base import Component, Message, split_host_port
from then.exceptions import ExecuteError


class SendMsgBot(sleekxmpp.ClientXMPP):
    def __init__(self, jid, password, recipient, message):
        sleekxmpp.ClientXMPP.__init__(self, jid, password)

        # The message we wish to send, and the JID that
        # will receive it.
        self.recipient = recipient
        self.msg = message

        # The session_start event will be triggered when
        # the bot establishes its connection with the server
        # and the XML streams are ready for use. We want to
        # listen for this event so that we we can initialize
        # our roster.
        self.add_event_handler("session_start", self.start)

    def start(self, event):
        """
        Process the session_start event.

        Typical actions for the session_start event are
        requesting the roster and broadcasting an initial
        presence stanza.

        Arguments:
            event -- An empty dictionary. The session_start
                     event does not provide any additional
                     data.
        """
        self.send_presence()
        self.get_roster()

        self.send_message(mto=self.recipient,
                          mbody=self.msg,
                          mtype='chat')

        # Using wait=True ensures that the send queue will be
        # emptied before ending the session.
        self.disconnect(wait=True)


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
        xmpp = SendMsgBot(self.component.from_,
                          self.component.password,
                          self.component.to,
                          self.body)
        xmpp.register_plugin('xep_0030')  # Service Discovery
        xmpp.register_plugin('xep_0199')  # XMPP Ping
        if self.component.server:
            server = split_host_port(self.component.server, 5222)
        elif self.component.from_.endswith('@gmail.com'):
            server = ('talk.google.com', 5222)
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
