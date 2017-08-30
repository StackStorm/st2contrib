from lib.base import AzureBaseStorageAction


class AzureDeleteContainerAction(AzureBaseStorageAction):
    def run(self, name):
        container = self._driver.get_container(container_name=name)
        result = self._driver.delete_container(container=container)
        return result
