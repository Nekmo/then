from io import TextIOWrapper
from then.exceptions import ConfigError


def parse_yaml(file: TextIOWrapper):
    from yaml import load, YAMLError
    try:
        from yaml import CLoader as Loader
    except ImportError:
        from yaml import Loader
    try:
        return load(file, Loader)
    except (UnicodeDecodeError, YAMLError) as e:
        raise ConfigError('{}'.format(e))
