from then.context import Context
from then.exceptions import ProgrammingError
from then.renders import FormatRenderMixin
from then.types import ItemTypes


def split_host_port(address, default_port=None, splitter=':'):
    parts = list(address.split(splitter))
    if len(parts) < 2:
        parts.append(default_port)
    parts[1] = int(parts[1])
    return parts


class MessageBase(object):
    def __init__(self, **kwargs):
        self.data = kwargs

    def get_init_data(self, locals):
        return {key: locals[key] for key in self.__class__.__init__.__code__.co_varnames if key != 'self'}

    def send(self, config):
        config.send(**self.data)


class ConfigBase(ItemTypes):
    def send(self, **kwargs):
        raise NotImplementedError


class TemplateBase(ItemTypes, FormatRenderMixin):
    message_class = None

    def get_message_class(self):
        if not self.message_class:
            raise NotImplementedError('Message class is undefined.')
        return self.message_class

    def __init__(self, **kwargs):
        super(TemplateBase, self).__init__(**kwargs)


class Component:
    _message_class = None
    _use_as = None

    def get_class(self):
        if not self._message_class:
            raise ProgrammingError('_message_class is undefined on {} component class.'.format(self.__class__.__name__))
        return self._message_class

    def message(self, context=None, **kwargs):
        if context is None:
            context = Context()
        context.update(**kwargs)
        cls = self.get_class()
        if cls._default_init:
            fields = cls.__dataclass_fields__
            msg_ctx = {key: context[key] for key in fields if key != 'component' and key in context}
            message = cls(component=self, **msg_ctx)
            message.add_extra({key: context[key] for key in context if key not in fields})
            return message
        else:
            return cls(component=self, **context)

    def send(self, context=None, **kwargs):
        return self.message(context, **kwargs).send()

    def copy(self):
        return self.__class__(**vars(self))

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


