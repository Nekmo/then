import json
from io import TextIOWrapper
from json import JSONDecodeError

from then.exceptions import ConfigError


def parse_json(file: TextIOWrapper):
    try:
        return json.load(file)
    except JSONDecodeError as e:
        raise ConfigError('{}'.format(e))
