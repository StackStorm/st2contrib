from lib.actions import BaseAction

__all__ = [
    'ListContainerClustersAction'
]


class ListContainerClustersAction(BaseAction):
    api_type = 'container'

    def run(self, credentials):
        driver = self._get_driver_for_credentials(credentials=credentials)
        members = driver.list_clusters()
        return self.resultsets.formatter(members)
