import os

from libcloud.storage.types import ContainerDoesNotExistError

from lib.actions import BaseAction

__all__ = [
    'UploadFileAction'
]


class UploadFileAction(BaseAction):
    api_type = 'storage'

    def run(self, credentials, file_path, container_name, object_name=None):
        driver = self._get_driver_for_credentials(credentials=credentials)

        try:
            container = driver.get_container(container_name=container_name)
        except ContainerDoesNotExistError:
            self.logger.debug('Container "%s" doesn\'t exist, creating it...' %
                              (container_name))
            container = driver.create_container(container_name=container_name)

        object_name = object_name if object_name else os.path.basename(file_path)
        obj = driver.upload_object(file_path=file_path, container=container,
                                   object_name=object_name)

        self.logger.info('Object successfully uploaded: %s' % (obj))
        return obj
