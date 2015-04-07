from lib.base import AzureBaseComputeAction
from lib.formatters import to_node_dict


class AzureListVMsAction(AzureBaseComputeAction):
    def run(self, cloud_service_name):
        nodes = self._driver.list_nodes(ex_cloud_service_name=cloud_service_name)
        nodes = [to_node_dict(node) for node in nodes]
        return nodes
