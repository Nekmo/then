from then.configs.components import LoadComponentConfigs
from then.exceptions import ThenError


class Then:
    def __init__(self, *args):
        if not args:
            raise ThenError('Sets configurations for components in Then class. '
                            'Currently there are no configurations')
        components_list = []
        for arg in args:
            if isinstance(arg, LoadComponentConfigs):
                components_list.extend(list(args))
            components_list.append(arg)
        self.components = {}
        for component in components_list:
            self.components[component.get_use_as()] = component
