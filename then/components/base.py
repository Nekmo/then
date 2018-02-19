from six import with_metaclass

from then.exceptions import ValidationError
from then.types import TypesMeta


class ComponentBase(with_metaclass(TypesMeta, object)):
    template_cls = None

    def __init__(self, **kwargs):
        types = self.__class__.types
        required = {key: value for key, value in types.items() if value.required}
        for key in required:
            if key not in kwargs:
                raise ValidationError('"{}" is a required option'.format(key))
        for key, value in kwargs.items():
            if key in types:
                value = types[key].clean(value)
            setattr(self, key, value)

    def get_template_cls(self):
        return self.template_cls

    def template(self):
        pass


class TemplateBase(object):
    def __init__(self, component):
        self.component = component
