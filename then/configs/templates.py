from dataclasses import dataclass
from typing import Type

from then.configs.base import LoadConfigBase
from then.templates.base import TemplateBase
from then.templates.format import FormatTemplate


@dataclass
class LoadTemplates(LoadConfigBase):
    path: str
    section: str = 'templates'
    template_class: Type[TemplateBase] = FormatTemplate

    schema = {
        'type': 'array',
        'items': {
            'type': 'object',
            'properties': {
                'params': {
                    'type': 'object',
                },
                'template_as': {
                    'type': 'string',
                }
            },
        }
    }

    def __post_init__(self):
        super().__post_init__()
        self.templates = self.get_templates()

    def get_templates(self):
        return [self.get_template(template_data) for template_data in self.data]

    def get_template(self, template_data: dict):
        template_name = template_data.get('template_as', 'default')
        template = self.template_class(**template_data.get('params', {}))
        if template_name:
            template.template_as(template_name)
        return template

    def __iter__(self):
        return iter(self.templates)
