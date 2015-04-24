from lib.action import BaseVMsAction
from lib.formatters import to_server_dict

__all__ = [
    'GetVMNamesAction'
]


class GetVMNamesAction(BaseVMsAction):
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

            result.append(item['name'])

        if count:
            return result[0:count]
        else:
            return result
