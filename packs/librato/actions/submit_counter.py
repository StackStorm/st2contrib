from lib import action

class LibratoSubmitCounter(action.LibratoBaseAction):
    def run(self, name, value, source):
        self.librato.submit(name, value, type='counter', source=source)
