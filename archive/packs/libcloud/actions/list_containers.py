from lib.actions import BaseAction

__all__ = [
    'ListContainersAction'
]


class ListContainersAction(BaseAction):
    api_type = 'container'

    def run(self, credentials, cluster_id=None):
        driver = self._get_driver_for_credentials(credentials=credentials)
        if cluster_id is not None:
            cluster = driver.get_cluster(cluster_id)
        else:
            cluster = None
        containers = driver.list_containers(cluster=cluster)
        return self.resultsets.formatter(containers)
