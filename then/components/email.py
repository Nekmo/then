from then.components.base import ComponentBase, TemplateBase
from then.types import EmailType, CharType


class EmailTemplate(TemplateBase):
    pass


class Email(ComponentBase):
    template_cls = EmailTemplate
    to = EmailType(required=True)
    from_ = EmailType(default='noreply@localhost')
    server = CharType(default='localhost')


print(Email())
