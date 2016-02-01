from lib.actions import BaseAction

__all__ = [
    'CreateContainerClusterAction'
]


class CreateContainerClusterAction(BaseAction):
    api_type = 'container'

    def run(self, credentials, name):
        driver = self._get_driver_for_credentials(credentials=credentials)

        record = driver.create_cluster(name=name)
        return self.resultsets.formatter(record)
