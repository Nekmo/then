#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `then` package."""
import unittest
from unittest.mock import patch

from then.components.email import Email, EmailMessage, get_default_config


class TestEmail(unittest.TestCase):
    to = 'test@localhost'
    subject = 'subject'
    body = 'body'

    def test_message_init(self):
        component = Email(self.to)
        message = EmailMessage(self.subject, self.body, component)
        self.assertEqual(message.message['subject'], self.subject)
        self.assertEqual(message.message.get_payload(), '{}\n'.format(self.body))
        self.assertEqual(message.message['from'], component.from_)
        self.assertEqual(message.message['to'], component.to)

    def test_default_config(self):
        address = 'foo@gmail.com'
        config = get_default_config(address)
        email = Email('bar@gmail.com', from_=address)
        self.assertEqual(email.tls, config['tls'])
        self.assertEqual(email.server, config['server'])

    @patch('then.components.email.SMTP', autospec=True)
    def test_send(self, m):
        msg = Email(self.to, server='myserver:888').message(subject=self.subject, body=self.body)
        msg.send()
        m.assert_called_with('myserver', 888)
        m.return_value.send_message.assert_called_once_with(msg.message, 'noreply@localhost', self.to)

    @patch('then.components.email.SMTP', autospec=True)
    def test_login(self, m):
        from_ = 'myuser@foo.com'
        password = 'password'
        Email(self.to, from_=from_, password=password, server='myserver:888').send()
        m.return_value.login.assert_called_once_with(from_, password)

    @patch('then.components.email.SMTP_SSL', autospec=True)
    def test_send_tls(self, m):
        msg = Email(self.to, server='secure:465', tls=True).message(subject=self.subject, body=self.body)
        msg.send()
        m.assert_called_with('secure', 465)

    def test_get_default_gmail_config(self):
        self.assertIsNotNone(get_default_config('foo@gmail.com'))

    def test_get_default_hotmail_config(self):
        self.assertIsNotNone(get_default_config('foo@hotmail.es'))
