#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `then` package."""
import unittest
from unittest.mock import patch

from then.components.email import Email, EmailMessage


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

    @patch('then.components.email.SMTP', autospec=True)
    def test_send(self, m):
        msg = Email(self.to, server='myserver:888').message(subject=self.subject, body=self.body)
        msg.send()
        m.assert_called_with('myserver', 888)
        m.return_value.send_message.assert_called_once_with(msg.message, 'noreply@localhost', self.to)
