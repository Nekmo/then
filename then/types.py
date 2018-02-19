import inspect
import re

from six import with_metaclass

from then.exceptions import ValidationError


class Type(object):
    def __init__(self, required=False, default=''):
        self.required = required
        self.default = default

    def validate(self, value):
        pass

    def to_python(self, value):
        return value

    def clean(self, value):
        value = self.to_python(value)
        self.validate(value)
        return value


class CharType(Type):
    def __init__(self, max_length=None, **kwargs):
        self.max_length = max_length
        super(CharType, self).__init__(**kwargs)


class EmailType(CharType):
    def validate(self, value):
        if value is None:
            return
        if not re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})?$', value):
            raise ValidationError('Invalid email: {}'.format(value))


class TypesMeta(type):
    def __new__(meta, name, bases, dct):
        meta.types = {key: value() if inspect.isclass(value) else value for key, value in dct.items()
                      if isinstance(value, Type) or (inspect.isclass(value) and issubclass(value, Type))}
        return super(TypesMeta, meta).__new__(meta, name, bases, dct)

    def __init__(cls, name, bases, dct):
        for key, value in list(vars(cls).items()):
            if isinstance(value, Type) or (inspect.isclass(value) and issubclass(value, Type)):
                delattr(cls, key)
        # dct = {key: value for key, value in dct.items()
        #        if not (isinstance(value, Type) or (inspect.isclass(value) and issubclass(value, Type)))}
        super(TypesMeta, cls).__init__(name, bases, dct)


class ItemTypes(with_metaclass(TypesMeta, object)):
    def __init__(self, **kwargs):
        types = self.__class__.types
        required = {key: value for key, value in types.items() if value.required}
        defaults = {key: value for key, value in types.items() if value.default}
        for key, value in defaults.items():
            if key not in kwargs:
                kwargs[key] = value.default
        for key in required:
            if key not in kwargs:
                raise ValidationError('"{}" is a required option'.format(key))
        for key, value in kwargs.items():
            if key in types:
                value = types[key].clean(value)
            setattr(self, key, value)
