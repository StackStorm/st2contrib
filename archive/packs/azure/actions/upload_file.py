import os

from libcloud.storage.types import ContainerDoesNotExistError

from lib.base import AzureBaseStorageAction
from lib.formatters import to_object_dict


class AzureUploadFileAction(AzureBaseStorageAction):
    def run(self, file_path, container_name, object_name=None):
        try:
            container = self._driver.get_container(container_name=container_name)
        except ContainerDoesNotExistError:
            self.logger.debug('Container "%s" doesn\'t exist, creating it...' %
                              (container_name))
            container = self._driver.create_container(container_name=container_name)

        object_name = object_name if object_name else os.path.basename(file_path)

        obj = self._driver.upload_object(file_path=file_path,
                                         container=container,
                                         object_name=object_name)
        obj = to_object_dict(obj)
        return obj
