from lib import action


class ConsulDeregisterServiceAction(action.ConsulBaseAction):
    def run(self, node, service, dc):

        result = self.consul.catalog.deregister(node, service, dc=dc)
        return (result, "")
