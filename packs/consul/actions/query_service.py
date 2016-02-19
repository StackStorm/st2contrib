from lib import action

class ConsulQueryServiceAction(action.ConsulBaseAction):
    def run(self, service, tag=None):
        index, service = self.consul.catalog.service(service, tag=tag)
        addresses = [node['Address'] for node in service]
        return ','.join(addresses)
