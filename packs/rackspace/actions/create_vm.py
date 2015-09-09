import random

from lib.action import PyraxBaseAction
from lib.formatters import to_server_dict

__all__ = [
    'CreateVMAction'
]


class CreateVMAction(PyraxBaseAction):
    def run(self, name, image_id, flavor_id, key_material=None, metadata=None,
            region=None):
        if region:
            cs = self.pyrax.connect_to_cloudservers(region=region)
        else:
            cs = self.pyrax.cloudservers

        image = cs.images.get(image_id)
        flavor = cs.flavors.get(flavor_id)

        if key_material:
            key_name = 'key-%s' % (random.randint(1, 100000))
            cs.keypairs.create(key_name, key_material)
        else:
            key_name = None

        self.logger.info('Creating server...')

        server = cs.servers.create(name=name, image=image, flavor=flavor,
                                   key_name=key_name, meta=metadata)

        # Block until provisioned
        self.pyrax.utils.wait_for_build(server)

        self.logger.info('Server successfully created: %s' % (server))

        result = to_server_dict(server=server)
        return result
