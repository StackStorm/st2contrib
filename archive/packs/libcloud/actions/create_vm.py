from libcloud.compute.base import NodeSize
from libcloud.compute.base import NodeLocation

from lib.actions import BaseAction

__all__ = [
    'CreateVMAction'
]


class CreateVMAction(BaseAction):
    api_type = 'compute'

    def run(self, credentials, name, size_id=None, image_id=None, size_name=None, image_name=None,
            location_id=None):
        driver = self._get_driver_for_credentials(credentials=credentials)
        location = NodeLocation(id=location_id, name=None,
                                country=None, driver=driver)

        if (not size_id and not size_name) or (size_id and size_name):
            raise ValueError('Either "size_id" or "size_name" needs to be provided')

        if (not image_id and not image_name) or (image_id and image_name):
            raise ValueError('Either "image_id" or "image_name" needs to be provided')

        if size_id is not None:
            size = NodeSize(id=size_id, name=None,
                            ram=None, disk=None, bandwidth=None,
                            price=None, driver=driver)
        elif size_name is not None:
            size = [s for s in driver.list_sizes() if size_name in s.name][0]

        if image_id is not None:
            image = [i for i in driver.list_images() if image_id == i.id][0]
        elif image_name is not None:
            image = [i for i in driver.list_images() if
                     image_name in i.extra.get('displaytext', i.name)][0]

        kwargs = {'name': name, 'size': size, 'image': image}

        if location_id:
            kwargs['location'] = location

        self.logger.info('Creating node...')

        node = driver.create_node(**kwargs)

        self.logger.info('Node successfully created: %s' % (node))
        return self.resultsets.formatter(node)
