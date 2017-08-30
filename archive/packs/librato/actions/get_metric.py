from lib import action


class LibratoGetMetric(action.LibratoBaseAction):
    def run(self, name, count=1, resolution=1):
        self.librato.get(name, count=count, resolution=resolution)
