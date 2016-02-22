from lib import action

class ListMetrics(action.LibratoBaseAction):
    def run(self):
        return self.librato.list_metrics()
