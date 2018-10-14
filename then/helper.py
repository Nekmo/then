from then.configs.components import LoadComponentConfigs
from then.exceptions import ThenError


class Templates:
    _use = 'default'

    def __init__(self, then, *args):
        self.then = then
        self.contexts = args
        self._args = {}

    def args(self, **kwargs):
        self._args = kwargs

    def use(self, use_name):
        contexts = self.copy()
        contexts._use = use_name
        return contexts

    def copy(self):
        contexts = Templates(self.then, *self.contexts)
        contexts._args = self._args
        contexts._use = self._use
        return contexts


class Then:
    def __init__(self, *args):
        if not args:
            raise ThenError('Sets configurations for components in Then class. '
                            'Currently there are no configurations')
        components_list = []
        for arg in args:
            if isinstance(arg, LoadComponentConfigs):
                components_list.extend(list(arg))
            else:
                components_list.append(arg)
        self.components = {}
        for component in components_list:
            self.components[component.get_use_as()] = component

    def templates(self, *args):
        return Templates(self, *args)
