from lib.action import PyraxBaseAction
from lib.formatters import to_server_dict

__all__ = [
    'GetVMIPsAction'
]

class GetVMIPsAction(PyraxBaseAction):
    def run(self, count=None, region=None, metadata=None):
        if region:
            cs = self.pyrax.connect_to_cloudservers(region=region)
        else:
            cs = self.pyrax.cloudservers

        servers = cs.list()

        result = []
        for server in servers:
            item = to_server_dict(server=server)

            if metadata:
                include = self._metadata_intersection(server=item,
                                                      metadata=metadata)

                if not include:
                    continue

            result.append(item['public_ips'][1])

        if count:
            return result[0:count]
        else:
            return result

    def _metadata_intersection(self, server, metadata):
        server_metadata = server.get('metadata', {})

        for key, value in metadata.items():
            server_metadata_value = server_metadata.get(key, None)

            if not server_metadata_value or server_metadata_value != value:
                return False

        return True
