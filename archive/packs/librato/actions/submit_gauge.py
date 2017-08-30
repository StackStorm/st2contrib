from lib import action


class LibratoSubmitGauge(action.LibratoBaseAction):
    def run(self, name, value, source):
        self.librato.submit(name, value, source=source)
