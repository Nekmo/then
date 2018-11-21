from then.params import Params
from then.exceptions import ProgrammingError


def split_host_port(address, default_port=None, splitter=':'):
    parts = list(address.split(splitter))
    if len(parts) < 2:
        parts.append(default_port)
    parts[1] = int(parts[1])
    return parts


class Component:
    _message_class = None
    _use_as = None
    _type = ''

    def get_class(self):
        if not self._message_class:
            raise ProgrammingError('_message_class is undefined on {} component class.'.format(self.__class__.__name__))
        return self._message_class

    def message(self, params=None, **kwargs):
        if params is None:
            params = Params()
        params.update(**kwargs)
        cls = self.get_class()
        if cls._default_init:
            fields = cls.__dataclass_fields__
            msg_ctx = {key: params[key] for key in fields if key != 'component' and key in params}
            message = cls(component=self, **msg_ctx)
            message.add_extra({key: params[key] for key in params if key not in fields})
            return message
        else:
            return cls(component=self, **params)

    def send(self, context=None, **kwargs):
        return self.message(context, **kwargs).send()

    def copy(self):
        return self.__class__(**{key: value for key, value in vars(self).items() if key in self.get_fields()})

    def use_as(self, name):
        component = self.copy()
        component._use_as = name
        return component

    def get_use_as(self):
        return self._use_as or self.get_default_use_as()

    def get_default_use_as(self):
        return self.__class__.__name__.lower()

    @property
    def name(self):
        return self.__class__.__name__

    @classmethod
    def get_fields(cls):
        return cls.__dataclass_fields__


class Message:
    component: Component = None
    _default_init = True
    extra = None

    def set_config(self, component: Component):
        self.component = component

    def add_extra(self, extra):
        self.extra = self.extra or {}
        self.extra.update(extra)

    def send(self):
        raise NotImplementedError


