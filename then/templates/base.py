from then.context import Params


class TemplateBase:
    def __init__(self, **kwargs):
        self.context = Params(**kwargs)
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
