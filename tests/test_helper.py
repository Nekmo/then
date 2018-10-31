import unittest
from unittest.mock import patch, Mock

from then.components import Telegram
from then.helper import Then, Templates
from then.templates.format import FormatTemplate


class TestTemplates(unittest.TestCase):
    def test_exact_template_name(self):
        template = FormatTemplate().template_as('foo')
        self.assertEqual(Templates(Mock(), template).use('foo').get_template(), template)

    def test_template_name(self):
        template = FormatTemplate().template_as('foo')
        self.assertEqual(Templates(Mock(), template).use('foo@bar').get_template(), template)


class TestThen(unittest.TestCase):
    @patch('then.components.Telegram.send')
    def test_send(self, m):
        Then(
            Telegram(token='foo', to='bar')
        ).templates(
            FormatTemplate(body='Hello {arg1}!')
        ).render(arg1='world').send()
        m.assert_called_once_with(dict(arg1='world', body='Hello world!'))

    def test_component_name(self):
        template = Telegram(token='foo', to='bar')
        then = Then(
            template
        )
        self.assertEqual(then.use('tpl@telegram').get_component(), template)
