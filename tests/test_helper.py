import unittest
from unittest.mock import patch

from then.components import Telegram
from then.helper import Then
from then.templates.format import FormatTemplate


class TestThen(unittest.TestCase):
    @patch('then.components.Telegram.send')
    def test_send(self, m):
        Then(
            Telegram(token='foo', to='bar')
        ).templates(
            FormatTemplate(body='Hello {arg1}!')
        ).render(arg1='world').send()
        m.assert_called_once_with(dict(arg1='world', body='Hello world!'))
