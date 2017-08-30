from lib.base import AzureBaseStorageAction
from lib.formatters import to_object_dict


class AzureListContainerObjectsAction(AzureBaseStorageAction):
    def run(self, name):
        container = self._driver.get_container(container_name=name)
        objects = self._driver.list_container_objects(container=container)
        objects = [to_object_dict(obj) for obj in objects]
        return objects
