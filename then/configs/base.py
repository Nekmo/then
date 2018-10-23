import os
import jsonschema
from dataclasses import dataclass
from typing import Union

from then.configs.json import parse_json
from then.configs.toml import parse_toml
from then.configs.yaml import parse_yaml
from then.exceptions import UnknownConfigFormatError, ConfigError

FORMATS = {
    'json': parse_json,
    'yaml': parse_yaml,
    'toml': parse_toml,
}
EXTENSIONS = {
    'json': 'json',
    'yaml': 'yaml',
    'toml': 'toml',
    'tml': 'toml',
    'yml': 'yaml',
}


def guess_format(file: str) -> str:
    if '.' not in file:
        raise UnknownConfigFormatError('Impossible to guess format for {}. '
                                       'Extension is not available.'.format(file))
    extension = file.split('.')[-1]
    if extension not in EXTENSIONS:
        raise UnknownConfigFormatError('Unknown extension {} in {}'
                                       'Available extensions: {}.'.format(extension, file, ', '.join(EXTENSIONS)))
    return EXTENSIONS[extension]


def open_file(path):
    if not os.path.lexists(path):
        raise ConfigError('Config path {} does not exists'.format(path))
    if not os.access(path, os.R_OK):
        raise ConfigError('Read permission denied to {}'.format(path))
    return open(path)


def validate_schema(data: dict, schema: Union[dict, None] = None):
    if not schema:
        return
    jsonschema.validate(data, schema)


class LoadConfigBase:
    path: str
    section: str = ''
    format: Union[str, None] = None

    data: Union[dict, list, None] = None

    schema: Union[dict, None] = None

    def __post_init__(self):
        format = (self.format or guess_format(self.path)).lower()
        if format not in FORMATS:
            raise UnknownConfigFormatError('Unknown format: {}'
                                           'Available formats: {}.'.format(format, ', '.join(FORMATS)))
        file = open_file(self.path)
        self.data = FORMATS[format](file)
        if not isinstance(self.data, dict):
            raise ConfigError('Invalid config data type: {}. Current data: {}'.format(type(self.data), self.data))
        if self.section:
            self.data = self.data[self.section]
        validate_schema(self.data, self.schema)


@dataclass
class LoadConfig(LoadConfigBase):
    path: str
    section: str = ''
    format: Union[str, None] = None

    data: Union[dict, list, None] = None

    schema: Union[dict, None] = None
