from then.templates.base import TemplateBase


class FormatTemplate(TemplateBase):

    def render(self):
        data = self._args.copy()
        data.update({key: value.format(**self._args) for key, value in self.params.items()})
        return data
