from lib.base import AzureBaseStorageAction
from lib.formatters import to_container_dict


class AzureListContainersAction(AzureBaseStorageAction):
    def run(self):
        containers = self._driver.list_containers()
        containers = [to_container_dict(container) for container in containers]
        return containers
