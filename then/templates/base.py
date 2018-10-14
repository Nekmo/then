from then.params import Params


class TemplateBase:
    _template_as = 'default'

    def __init__(self, **kwargs):
        self.params = Params(**kwargs)
        self._args = {}
        self._render = None

    def args(self, **kwargs):
        self._args.update(**kwargs)

    def render(self):
        raise NotImplementedError

    def get_cached_render(self):
        if self._render is None:
            self._render = self.render()
        return self._render

    def __getitem__(self, item):
        return self.get_cached_render()[item]

    def __contains__(self, item):
        return item in self.get_cached_render()

    def __iter__(self):
        return self.get_cached_render()

    def template_as(self, template_as):
        self._template_as = template_as
