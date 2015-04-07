from libcloud.compute.base import Node

from lib.base import AzureBaseComputeAction


class AzureDestroyVMAction(AzureBaseComputeAction):
    def run(self, vm_id, cloud_service_name, deployment_slot=None):
        node = Node(id=vm_id, name=None, state=None, public_ips=None,
                    private_ips=None, driver=self._driver)
        result = self._driver.destroy_node(node=node,
                                           ex_cloud_service_name=cloud_service_name,
                                           ex_deployment_slot=deployment_slot)
        return result
