from lib.base import AzureBaseStorageAction
from lib.formatters import to_container_dict


class AzureCreateContainerAction(AzureBaseStorageAction):
    def run(self, name):
        container = self._driver.create_container(container_name=name)
        container = to_container_dict(container)
        return container
