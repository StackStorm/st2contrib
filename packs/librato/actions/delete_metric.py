from lib import action

class LibratoDeleteMetric(action.LibratoBaseAction):
    def run(self, name):
        return self.librato.delete(name)

