from collections import defaultdict

from then.configs.components import LoadComponentConfigs
from then.configs.templates import LoadTemplates
from then.exceptions import ThenError, InvalidUsage
from then.utils import flat_list


DEFAULT = 'default'


class Templates:
    _use = DEFAULT

    def __init__(self, then, *args):
        self.then = then
        self._templates = defaultdict(list)
        for arg in args:
            self._templates[arg.get_template_name()].append(arg)
        self._args = {}

    def render(self, **kwargs):
        templates = self.copy()
        templates._args = kwargs
        return templates

    def use(self, use_name):
        templates = self.copy()
        templates._use = use_name
        return templates

    def _get_use_name(self):
        parts = self._use.split('@', 1)
        if len(parts) > 1:
            template_name, component_name = parts
        else:
            template_name, component_name = None, parts[0]
        template_name = template_name or DEFAULT
        component_name = component_name or DEFAULT
        return template_name, component_name

    def get_template(self):
        if self._use in self._templates:
            # TODO: use component_name for get the best template using params
            return self._templates[self._use][-1]
        template_name, component_name = self._get_use_name()
        if template_name in self._templates:
            return self._templates[template_name][-1]

    def copy(self):
        templates = Templates(self.then, *self._templates.values())
        templates._args = self._args
        templates._use = self._use
        return templates

    def send(self):
        raise NotImplementedError


class Then:
    _use = DEFAULT

    def __init__(self, *args):
        if not args:
            raise ThenError('Sets configurations for components in Then class. '
                            'Currently there are no configurations')
        components_list = flat_list(args, (tuple, list, LoadComponentConfigs))
        self.components = {}
        for component in components_list:
            self.components[component.get_use_as()] = component

    def templates(self, *args):
        args = flat_list(args, (tuple, list, LoadTemplates))
        return Templates(self, *args)

    def use(self, use_name):
        then = self.copy()
        then._use = use_name
        return then

    def copy(self):
        then = Then(*self.components)
        then._use = self._use
        return then

    def get_component(self):
        if not self.components:
            raise InvalidUsage('There are no configurations. Registers configs using '
                               'Then(<component config>)')
        if self._use == DEFAULT and len(self.components) > 1:
            raise InvalidUsage('There is more than one configuration available. '
                               'Use the use("<config>") option')
        return self.components[self._use]

    def send(self, params=None):
        self.get_component().send(params)
