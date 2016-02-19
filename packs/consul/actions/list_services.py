from lib import action

class ConsulListServicesAction(action.ConsulBaseAction):
    def run(self):
        index, services = self.consul.catalog.services()
        return services
