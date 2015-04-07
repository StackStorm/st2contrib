from lib.base import AzureBaseStorageAction


class AzureDeleteObjectAction(AzureBaseStorageAction):
    def run(self, container_name, object_name):
        obj = self._driver.get_object(container_name=container_name,
                                      object_name=object_name)
        result = self._driver.delete_object(obj=obj)
        return result
