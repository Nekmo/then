import io
import unittest
from unittest.mock import patch, Mock

from then.configs.json import parse_json
from then.configs.yaml import parse_yaml
from then.exceptions import ConfigError


class TestJson(unittest.TestCase):
    @patch('json.load')
    def test_parse(self, m):
        parse_json(Mock())
        m.assert_called_once()

    def test_exception(self):
        with self.assertRaises(ConfigError):
            parse_yaml(io.StringIO('{{'))
