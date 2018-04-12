from then.types import CharType


class FormatRenderMixin(object):
    def render(self, **kwargs):
        items = {}
        for key, value in self.__class__.types.items():
            if isinstance(value, CharType):
                items[key] = getattr(self, key).format(**kwargs)
            else:
                items[key] = getattr(self, key)
        return self.get_message_class()(**items)
