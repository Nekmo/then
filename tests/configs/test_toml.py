import io
import unittest
from unittest.mock import patch, Mock

from then.configs.toml import parse_toml
from then.exceptions import ConfigError


class TestToml(unittest.TestCase):
    @patch('toml.load')
    def test_parse(self, m):
        parse_toml(Mock())
        m.assert_called_once()

    def test_exception(self):
        with self.assertRaises(ConfigError):
            parse_toml(io.StringIO('<=,'))
