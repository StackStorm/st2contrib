from azure.mgmt.resource.resources import (
    ResourceManagementClient,
    ResourceManagementClientConfiguration)
from azure.mgmt.resource.resources.models import GenericResource

from lib.base import AzureBaseResourceManagerAction


class CreateResourceAction(AzureBaseResourceManagerAction):
    def run(self, subscription_id, group_name, resource_name,
            resource_provider_namespace, resource_type, parent_resource_path,
            api_version, location):
        credentials = self.credentials

        resource_client = ResourceManagementClient(
            ResourceManagementClientConfiguration(
                credentials,
                subscription_id))

        result = resource_client.resources.create_or_update(
            group_name,
            resource_provider_namespace=resource_provider_namespace,
            parent_resource_path=parent_resource_path,
            resource_type=resource_type,
            resource_name=resource_name,
            api_version=api_version,
            parameters=GenericResource(
                location=location,
                properties={},
            ),
        )
        return result
