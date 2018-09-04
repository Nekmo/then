from dataclasses import dataclass

from then.configs.base import LoadConfigBase


@dataclass
class LoadComponentConfigs(LoadConfigBase):
    path: str
    section: str = 'components'

    schema = {
        'type': 'array',
        'items': {
            'type': 'object',
            'properties': {
                'component': {
                    'type': 'string',
                },
                'config': {
                    'type': 'object',
                },
                'use_as': {
                    'type': 'string',
                }
            },
            'required': ['component']
        }
    }

    def __post_init__(self):
        super().__post_init__()
