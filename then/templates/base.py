from then.params import Params


class TemplateBase(dict):
    _template_as = None

    def __init__(self, **kwargs):
        self.params = Params(**kwargs)
        self._args = {}
        self._render = None
        super().__init__()

    def args(self, **kwargs):
        self._args.update(**kwargs)
        self.clear()
        self.update(self.render_template())
        return self
        # return self

    def render_template(self):
        raise NotImplementedError

    def get_default_template_name(self):
        return 'default'

    def get_template_name(self):
        return self._template_as or self.get_default_template_name()

    def template_as(self, template_as):
        self._template_as = template_as
        return self
