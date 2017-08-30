from lib.action import BaseVMsAction

__all__ = [
    'SetVMMetadata'
]


class SetVMMetadata(BaseVMsAction):
    def run(self, vm_id, metadata, region=None):
        metadata = metadata or {}

        if region:
            cs = self.pyrax.connect_to_cloudservers(region=region)
        else:
            cs = self.pyrax.cloudservers

        server = cs.servers.get(vm_id)

        removed_metadata_keys = set(server.metadata.keys()).difference(metadata.keys())
        removed_metadata_keys = list(removed_metadata_keys)

        cs.servers.delete_meta(server, removed_metadata_keys)
        cs.servers.set_meta(server, metadata)

        return True
