from libcloud.compute.base import NodeSize
from libcloud.compute.base import NodeImage
from libcloud.compute.base import NodeLocation

from lib.actions import BaseAction

__all__ = [
    'CreateVMAction'
]


class CreateVMAction(BaseAction):
    api_type = 'compute'

    def run(self, credentials, name, size_id=None, image_id=None,
            size_name=None, image_name=None, location_id=None):
        driver = self._get_driver_for_credentials(credentials=credentials)
        location = NodeLocation(id=location_id, name=None,
                                country=None, driver=driver)
        self.logger.info('Creating node...')

        if size_id != None and image_id != None:
            image = NodeImage(id=image_id, name=None,
                              driver=driver)
            size = NodeSize(id=size_id, name=None,
                            ram=None, disk=None, bandwidth=None,
                            price=None, driver=driver)

            kwargs = {'name': name, 'size': size, 'image': image}

        if size_name != None and image_name != None:
            image = [i for i in driver.list_images() if i.extra['displaytext'] == image_name][0]
            size = [s for s in driver.list_sizes() if s.name == size_name][0]

            kwargs = {'name': name, 'size': size, 'image': image}

        if location_id:
            kwargs['location'] = location

        node = driver.create_node(**kwargs)

        self.logger.info('Node successfully created: %s' % (node))
        return node
