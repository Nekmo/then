#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `then` package."""


import unittest

from then.components.email import Email, EmailMessage


class TestEmail(unittest.TestCase):
    subject = 'subject'
    body = 'body'

    def test_message_init(self):
        component = Email('test@localhost')
        message = EmailMessage(self.subject, self.body, component)
        self.assertEqual(message.message['subject'], self.subject)
        self.assertEqual(message.message.get_payload(), '{}\n'.format(self.body))
        self.assertEqual(message.message['from'], component.from_)
        self.assertEqual(message.message['to'], component.to)
