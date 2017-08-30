from lib import actions
from time import sleep

__all__ = [
    'WaitForCAASServerOperationAction',
]


class WaitForCAASServerOperationAction(actions.BaseAction):

    def run(self, region, id):
        node = self.getNode(region, id)
        if node is not None:
            while(node.extra['status'].action == 'None'):
                sleep(5)
                node = self.getNode(region, id)
        else:
            raise "VM with the name doesn't exist"

    def getNode(self, region, id):
        driver = self._get_compute_driver(region)
        node = driver.ex_get_node_by_id(id)
        return node
