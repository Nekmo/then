import io
import unittest
from unittest.mock import patch, Mock

from then.configs.yaml import parse_yaml
from then.exceptions import ConfigError


class TestYaml(unittest.TestCase):
    @patch('yaml.load')
    def test_parse(self, m):
        parse_yaml(Mock())
        m.assert_called_once()

    def test_exception(self):
        with self.assertRaises(ConfigError):
            parse_yaml(io.StringIO('dmKLq,<\n\x00'))
