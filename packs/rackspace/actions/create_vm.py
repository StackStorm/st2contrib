import random

from lib.action import PyraxBaseAction

__all__ = [
    'CreateVMAction'
]


class CreateVMAction(PyraxBaseAction):
    def run(self, name, image_id, flavor_id, key_material=None):
        cs = self.pyrax.cloudservers

        image = cs.images.get(image_id)
        flavor = cs.flavors.get(flavor_id)

        if key_material:
            key_name = 'key-%s' % (random.randint(1, 100000))
            key_pair = cs.keypairs.create(key_name, key_material)
        else:
            key_name = None

        self.logger.info('Creating server...')

        server = cs.servers.create(name=name, image=image, flavor=flavor,
                                   key_name=key_name)

        # Block until provisioned
        self.pyrax.utils.wait_for_build(server)

        self.logger.info('Server successfully created: %s' % (server))

        public_ips = [ip['addr'] for ip in server.addresses['public']]
        private_ips = [ip['addr'] for ip in server.addresses['private']]

        result = {
            'id': server.id,
            'name': server.name,
            'status': server.status,
            'image_id': server.image['id'],
            'flavor_id': server.flavor['id'],
            'public_ips': public_ips,
            'private_ips': private_ips,
            'key_name': server.key_name
        }

        return result
