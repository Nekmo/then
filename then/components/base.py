
from then.exceptions import ValidationError
from then.types import ItemTypes


class ComponentBase(ItemTypes):
    template_cls = None

    def get_template_cls(self):
        return self.template_cls

    def template(self, **kwargs):
        return self.get_template_cls()(self, **kwargs)


class TemplateBase(ItemTypes):
    def __init__(self, component, **kwargs):
        self.component = component
        super(TemplateBase, self).__init__(**kwargs)

    def send(self, **kwargs):
        raise NotImplementedError
