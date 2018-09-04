from dataclasses import dataclass

from then.components import get_component_by_name
from then.configs.base import LoadConfigBase
from then.exceptions import ConfigError


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
        self.components = self.get_components()

    def get_components(self):
        return [self.get_component(component_data) for component_data in self.data]

    def get_component(self, component_data: dict):
        component_name = component_data['component']
        try:
            component_class = get_component_by_name(component_name)
        except KeyError:
            raise ConfigError('Invalid component {} on {}'.format(component_name, component_data))
        component = component_class(**component_data.get('config', {}))
        if 'use_as' in component_data:
            component = component.use_as(component_data['use_as'])
        return component

    def __iter__(self):
        return self.components
