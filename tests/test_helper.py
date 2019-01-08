import unittest
from unittest.mock import patch, Mock

from then.components import Telegram
from then.helper import Then, Templates
from then.templates.format import FormatTemplate


class TestTemplates(unittest.TestCase):
    def get_then_mock(self, type='message'):
        mock = Mock()
        mock.get_component.return_value._type = type
        return mock

    def test_exact_template_name(self):
        template = FormatTemplate().template_as('foo')
        self.assertEqual(Templates(self.get_then_mock(), template).use('foo').get_template(), template)

    def test_template_name(self):
        template = FormatTemplate().template_as('foo')
        self.assertEqual(Templates(self.get_then_mock(), template).use('foo@bar').get_template(), template)

    def test_default_template(self):
        template = FormatTemplate()
        template2 = FormatTemplate().template_as('tpl2')
        self.assertEqual(Templates(self.get_then_mock(), template, template2).use('bar').get_template(), template)


class TestThen(unittest.TestCase):
    @patch('then.components.Telegram.send')
    def test_send(self, m):
        templates = Then(
            Telegram(token='foo', to='bar')
        ).templates(
            FormatTemplate(body='Hello {arg1}!')
        )
        render = templates.get_template().args(arg1='world')
        templates.render(arg1='world').send()
        m.assert_called_once_with(render)

    def test_component_name(self):
        component = Telegram(token='foo', to='bar')
        then = Then(
            component
        )
        self.assertEqual(then.use('tpl@telegram').get_component(), component)
