from then.templates.base import TemplateBase


class FormatTemplate(TemplateBase):

    def render(self):
        return {key: value.format(self._args) for key, value in self.params.items()}
