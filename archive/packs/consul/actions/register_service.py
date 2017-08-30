from lib import action


class ConsulRegisterServiceAction(action.ConsulBaseAction):
    def run(self, node, service, address, port, tags, dc):

        definition = {"Service": service, "Port": port, "Tags": tags}
        result = self.consul.catalog.register(node, address, service=definition, dc=dc)
        return (result, "")
