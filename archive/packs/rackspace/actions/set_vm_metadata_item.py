from lib.action import BaseVMsAction

__all__ = [
    'SetVMMetadataItem'
]


class SetVMMetadataItem(BaseVMsAction):
    def run(self, vm_id, key, value, region=None):
        if region:
            cs = self.pyrax.connect_to_cloudservers(region=region)
        else:
            cs = self.pyrax.cloudservers

        server = cs.servers.get(vm_id)

        metadata = server.metadata or {}
        metadata[key] = value

        cs.servers.set_meta(server, metadata)

        return True
