from lib import action


class ConsulQueryNodeAction(action.ConsulBaseAction):
    def run(self, node):
        index, node = self.consul.catalog.node(node)
        return node
