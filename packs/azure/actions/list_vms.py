from lib.base import AzureBaseAction
from lib.formatters import to_node_dict


class AzureListVMsAction(AzureBaseAction):
    def run(self, cloud_service_name):
        nodes = self._driver.list_nodes(ex_cloud_service_name=cloud_service_name)
        nodes = [to_node_dict(node) for node in nodes]
        return nodes
