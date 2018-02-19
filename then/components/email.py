from then.components.base import ComponentBase, TemplateBase
from then.types import EmailType, CharType


class EmailTemplate(TemplateBase):
    subject = CharType
    body = CharType

    def render(self, **kwargs):
        items = {}
        for key, value in self.__class__.types:
            if isinstance(value, CharType):
                items[key] = getattr(self, key).format(**kwargs)
            else:
                items[key] = getattr(self, key)
        return items

    def send(self, **kwargs):
        items = self.render(**kwargs)


class Email(ComponentBase):
    template_cls = EmailTemplate
    to = EmailType(required=True)
    from_ = EmailType(default='noreply@localhost')
    server = CharType(default='localhost')


tpl = Email(to='nekmo@localhost')
tpl.template(subject='{name}', body='Body: {name}').send(name='foo')
