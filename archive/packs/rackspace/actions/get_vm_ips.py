from lib.action import BaseVMsAction
from lib.formatters import to_server_dict

__all__ = [
    'GetVMIPsAction'
]


class GetVMIPsAction(BaseVMsAction):
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

            public_ips = item.get('public_ips', [])
            result.extend(public_ips)

        if count:
            return result[0:count]
        else:
            return result
