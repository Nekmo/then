#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `then` package."""
import unittest
from unittest.mock import patch

from then.components import Audio


class TestAudio(unittest.TestCase):

    @patch('then.components.audio.AudioMessage.get_next', autospec=True,
           return_value='file.mp3')
    def test_get_cmd(self, m):
        file = 'file.mp3'
        message = Audio().message(path=file)
        self.assertEqual(message.get_cmd(),
                         ["ffplay", "-nodisp", "-autoexit", file])
        m.assert_called_once()
