from then.params import Params


class TemplateBase:
    _template_as = None

    def __init__(self, **kwargs):
        self.params = Params(**kwargs)
        self._args = {}
        self._render = None

    def args(self, **kwargs):
        self._args.update(**kwargs)
        return self

    def render_template(self):
        raise NotImplementedError

    def get_cached_render(self):
        if self._render is None:
            self._render = self.render_template()
        return self._render

    def __getitem__(self, item):
        return self.get_cached_render()[item]

    def __contains__(self, item):
        return item in self.get_cached_render()

    def __iter__(self):
        yield from self.get_cached_render().items()

    def __eq__(self, other):
        return dict(other) == dict(self)

    def get_default_template_name(self):
        return 'default'

    def get_template_name(self):
        return self._template_as or self.get_default_template_name()

    def template_as(self, template_as):
        self._template_as = template_as
        return self
