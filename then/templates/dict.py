from then.templates.base import TemplateBase


class DictTemplate(TemplateBase):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.args()

    def render_template(self):
        data = dict(self.params)
        data.update(self._args)
        return data
