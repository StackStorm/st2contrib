from lib import action


class ConsulListNodesAction(action.ConsulBaseAction):
    def run(self):
        index, nodes = self.consul.catalog.nodes()
        return nodes
