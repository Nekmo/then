#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `then` package."""
import unittest
from unittest.mock import patch, ANY

from then.components.xmpp import Xmpp, SendMsgBot, GOOGLE_SERVER
from then.exceptions import ExecuteError

FROM: str = 'account1@gmail.com'
PASSWORD: str = 'mypass'
TO: str = 'account2@gmail.com'
BODY: str = 'My message'


class TestSendMsgBot(unittest.TestCase):
    from_: str = FROM
    password: str = PASSWORD
    to: str = TO
    body: str = BODY

    @patch('then.components.xmpp.SendMsgBot.send_presence', autospec=True)
    @patch('then.components.xmpp.SendMsgBot.get_roster', autospec=True)
    @patch('then.components.xmpp.SendMsgBot.send_message', autospec=True)
    @patch('then.components.xmpp.SendMsgBot.disconnect', autospec=True)
    def test_start(self, m1, m2, m3, m4):
        send_msg_bot = SendMsgBot(self.from_, self.password, self.to, self.body)
        send_msg_bot.start(None)
        m4.assert_called_once()
        m3.assert_called_once()
        m2.assert_called_once_with(send_msg_bot, mto=self.to, mbody=self.body, mtype='chat')
        m1.assert_called_once_with(send_msg_bot, wait=True)


class TestXmpp(unittest.TestCase):
    from_: str = FROM
    password: str = PASSWORD
    to: str = TO
    body: str = BODY

    def get_component(self, **kwargs):
        return Xmpp(self.from_, self.password, self.to, **kwargs)

    @patch('then.components.xmpp.SendMsgBot.connect', autospec=True, return_value=True)
    @patch('then.components.xmpp.SendMsgBot.process', autospec=True)
    def test_send(self, m1, m2):
        self.get_component().send(body=self.body)
        m2.assert_called_once_with(ANY, GOOGLE_SERVER)
        m1.assert_called_once()

    @patch('then.components.xmpp.SendMsgBot.connect', autospec=True, return_value=True)
    @patch('then.components.xmpp.SendMsgBot.process', autospec=True)
    def test_server(self, m1, m2):
        self.get_component(server='server:9999').send(body=self.body)
        m2.assert_called_once_with(ANY, ['server', 9999])
        m1.assert_called_once()

    @patch('then.components.xmpp.SendMsgBot.connect', autospec=True, return_value=True)
    @patch('then.components.xmpp.SendMsgBot.process', autospec=True)
    def test_auto_server(self, m1, m2):
        Xmpp('foo@server', self.password, self.to).send(body=self.body)
        m2.assert_called_once_with(ANY, ())
        m1.assert_called_once()

    @patch('then.components.xmpp.SendMsgBot.connect', autospec=True, return_value=False)
    def test_connect_error(self, m1):
        with self.assertRaises(ExecuteError):
            self.get_component().send(body=self.body)
