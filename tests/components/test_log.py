import unittest
from logging import FileHandler, StreamHandler, Formatter
from unittest.mock import patch

from then.components import Log
from then.exceptions import ValidationError


class TestLog(unittest.TestCase):

    @patch('then.components.log.logging.getLogger', autospec=True)
    def test_send_debug(self, m):
        component = Log()
        component.debug('foo')
        m.return_value.debug.assert_called_once_with('foo')

    @patch('then.components.log.logging.getLogger', autospec=True)
    def test_send_info(self, m):
        component = Log()
        component.info('foo')
        m.return_value.info.assert_called_once_with('foo')

    @patch('then.components.log.logging.getLogger', autospec=True)
    def test_send_warning(self, m):
        component = Log()
        component.warning('foo')
        m.return_value.warning.assert_called_once_with('foo')

    @patch('then.components.log.logging.getLogger', autospec=True)
    def test_send_error(self, m):
        component = Log()
        component.error('foo')
        m.return_value.error.assert_called_once_with('foo')

    @patch('then.components.log.logging.getLogger', autospec=True)
    def test_send_critical(self, m):
        component = Log()
        component.critical('foo')
        m.return_value.critical.assert_called_once_with('foo')

    def test_file_handler(self):
        filename = '/tmp/output.log'
        component = Log(filename)
        self.assertEqual(len(component.logger.handlers), 1)
        self.assertIsInstance(component.logger.handlers[0], FileHandler)
        self.assertEqual(component.logger.handlers[0].baseFilename, filename)

    def test_console_handler(self):
        component = Log(console=True)
        self.assertEqual(len(component.logger.handlers), 1)
        self.assertIsInstance(component.logger.handlers[0], StreamHandler)

    def test_formatter(self):
        component = Log(console=True)
        self.assertIsInstance(component.logger.handlers[0].formatter, Formatter)
        self.assertEqual(component.logger.handlers[0].formatter._fmt, component.formatter)

    def test_invalid_logger(self):
        with self.assertRaises(ValidationError):
            Log().send(level='spam', body='foo')
