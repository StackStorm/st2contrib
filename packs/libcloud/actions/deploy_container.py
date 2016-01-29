from libcloud.container.utils.docker import HubClient

from lib.actions import BaseAction

__all__ = [
    'DeployContainerAction'
]


class DeployContainerAction(BaseAction):
    api_type = 'container'

    def run(self, credentials, name, repository_name, tag,
            start, cluster_id=None, parameters=None):
        driver = self._get_driver_for_credentials(credentials=credentials)
        hub_client = HubClient()
        image = hub_client.get_image(repository_name, tag)
        if cluster_id is not None:
            cluster = driver.get_cluster(cluster_id)
        else:
            cluster = None
        record = driver.deploy_container(name=name, image=image,
                                         start=start, cluster=cluster,
                                         parameters=parameters)
        return self.resultsets.formatter(record)
