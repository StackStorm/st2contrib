from lib.action import PyraxBaseAction
from lib.formatters import to_server_dict

__all__ = [
    'ListVMsAction'
]


class ListVMsAction(PyraxBaseAction):
    def run(self, region=None):
        if region:
            cs = self.pyrax.connect_to_cloudservers(region=region)
        else:
            cs = self.pyrax.cloudservers

        servers = cs.list()

        result = []
        for server in servers:
            item = to_server_dict(server=server)
            result.append(item)

        return result
