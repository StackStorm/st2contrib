from libcloud.compute.base import NodeSize
from libcloud.compute.base import NodeImage

from lib.base import AzureBaseComputeAction


class AzureCreateVMAction(AzureBaseComputeAction):
    def run(self, name, size_id, image_id, cloud_service_name,
            storage_service_name=None, new_deployment=False,
            deployment_slot='Production', deployment_name=None,
            admin_user_id='azureuser'):
        size = NodeSize(id=size_id, name=None, ram=None, disk=None,
                        bandwidth=None, price=None, driver=self._driver)
        image = NodeImage(id=image_id, name=None, driver=self._driver)
        node = self._driver.create_node(name=name, size=size, image=image,
                                        ex_cloud_service_name=cloud_service_name,
                                        ex_storage_service_name=storage_service_name,
                                        ex_new_deployment=new_deployment,
                                        ex_deployment_slot=deployment_slot,
                                        ex_deployment_name=deployment_name,
                                        ex_admin_user_id=admin_user_id)
        return node
