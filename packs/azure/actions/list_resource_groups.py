from azure.mgmt.resource import (
    ResourceManagementClient,
    ResourceManagementClientConfiguration)
from lib.base import AzureBaseResourceManagerAction


class ListResourceGroupsAction(AzureBaseResourceManagerAction):
    def run(self, subscription_id):
        credentials = self.credentials

        resource_client = ResourceManagementClient(
            ResourceManagementClientConfiguration(
                credentials,
                subscription_id))

        resource_groups = resource_client.resource_groups.list()
        return [group.name for group in resource_groups]
