import copy
from collections import defaultdict
from typing import Type

from then.configs.components import LoadComponentConfigs
from then.configs.templates import LoadTemplates
from then.exceptions import ThenError, InvalidUsage
from then.params import Params
from then.templates.base import TemplateBase
from then.utils import flat_list


DEFAULT = 'default'


class UseBase:
    _use = DEFAULT

    def use(self, use_name):
        instance = self.copy()
        instance._use = use_name
        return instance

    def _get_use_name(self, use=None, default_template=True):
        parts = (use or self._use).split('@', 1)
        if len(parts) > 1:
            template_name, component_name = parts
        else:
            template_name, component_name = None, parts[0]
        if default_template:
            template_name = template_name or DEFAULT
        component_name = component_name or DEFAULT
        return template_name, component_name

    def copy(self):
        raise NotImplementedError


class Templates(UseBase):

    def __init__(self, then, *args):
        self.then = then
        self._templates = defaultdict(list)
        for arg in args:
            self._templates[arg.get_template_name()].append(arg)
        self._args = args
        self._render_params = {}

    def render(self, **kwargs):
        templates = self.copy()
        templates._render_params = kwargs
        return templates

    def get_template(self) -> TemplateBase:
        if self._use in self._templates:
            # TODO: use component_name for get the best template using params
            return self._templates[self._use][-1]
        template_name, component_name = self._get_use_name(default_template=False)
        component = None
        if not template_name:
            component = self.then.get_component(component_name)
        if not template_name and component and component._type != 'message':
            return TemplateBase()
        elif not template_name:
            template_name = component_name
        if template_name in self._templates:
            return self._templates[template_name][-1]
        return TemplateBase()

    def copy(self):
        templates = Templates(self.then, *copy.copy(self._args))
        templates._render_params = self._render_params
        templates._use = self._use
        return templates

    def send(self):
        component_name = self._get_use_name()[1]
        params = self.get_template().args(**self._render_params)
        self.then.use(component_name).send(params)


class Then(UseBase):

    def __init__(self, *args):
        if not args:
            raise ThenError('Sets configurations for components in Then class. '
                            'Currently there are no configurations')
        components_list = flat_list(args, (tuple, list, LoadComponentConfigs))
        self.components = {}
        for component in components_list:
            self.components[component.get_use_as()] = component
        self._args = args

    def templates(self, *args):
        args = flat_list(args, (tuple, list, LoadTemplates))
        return Templates(self, *args)

    def copy(self):
        then = Then(*self._args)
        then._use = self._use
        return then

    def get_component(self, use=None):
        use = use or self._use
        if not self.components:
            raise InvalidUsage('There are no configurations. Registers configs using '
                               'Then(<component config>)')
        if use == DEFAULT and len(self.components) > 1:
            raise InvalidUsage('There is more than one configuration available. '
                               'Use the use("<config>") option')
        elif use == DEFAULT:
            return next(iter(self.components.values()))
        template_name, component_name = self._get_use_name()
        if component_name in self.components:
            return self.components[component_name]
        return self.components[use]

    def send(self, params=None):
        self.get_component().send(params)
