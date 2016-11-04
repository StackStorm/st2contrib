from lib import action


class ConsulQueryServiceAction(action.ConsulBaseAction):
    def run(self, service, tag=None, ports=False):
        index, service = self.consul.catalog.service(service, tag=tag)
        if ports:
            addresses = ["{}:{}".format(node['Address'], node['ServicePort']) for node in service]
        else:
            addresses = [node['Address'] for node in service]
        return ','.join(addresses)
