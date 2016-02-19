from lib import action

class ConsulListDatacentersAction(action.ConsulBaseAction):
    def run(self):
        return self.consul.catalog.datacenters()
