from azure.mgmt.resource import (
    ResourceManagementClient,
    ResourceManagementClientConfiguration)
from azure.mgmt.resource import Deployment
from azure.mgmt.resource import DeploymentProperties
from azure.mgmt.resource import DeploymentMode
from azure.mgmt.resource import ParametersLink
from azure.mgmt.resource import TemplateLink

from lib.base import AzureBaseResourceManagerAction


class AzureCreateLinkedResourceUriAction(AzureBaseResourceManagerAction):
    def run(self, subscription_id, deployment_name, group_name,
            template_uri, parameters_uri):
        credentials = self.credentials
        resource_client = ResourceManagementClient(
            ResourceManagementClientConfiguration(
                credentials,
                subscription_id))
        template = TemplateLink(
            uri=template_uri,
        )

        parameters = ParametersLink(
            uri=parameters_uri,
        )
        result = resource_client.deployments.create_or_update(
            group_name,
            deployment_name,
            Deployment(
                properties=DeploymentProperties(
                    mode=DeploymentMode.incremental,
                    template_link=template,
                    parameters_link=parameters,
                )
            )
        )
        return result
