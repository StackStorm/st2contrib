from lib import action


class ConsulRegisterServiceAction(action.ConsulBaseAction):
    def run(self, nid, name, address, port, tags, dc):

        definition = { "Service": name, "Port": port, "Tags": tags }
        result = self.consul.catalog.register(nid, address, service=definition, dc=dc)
        return result
