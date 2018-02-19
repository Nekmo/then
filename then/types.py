import inspect
import re

from then.exceptions import ValidationError


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
