from io import TextIOWrapper

from then.exceptions import ConfigError


def parse_toml(file: TextIOWrapper):
    import toml
    from toml import TomlDecodeError
    try:
        return toml.load(file)
    except TomlDecodeError as e:
        raise ConfigError('{}'.format(e))
