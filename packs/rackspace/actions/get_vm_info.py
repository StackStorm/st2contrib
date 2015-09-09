from lib.action import PyraxBaseAction
from lib.formatters import to_server_dict

__all__ = [
    'GetVMInfoAction'
]


class GetVMInfoAction(PyraxBaseAction):
    def run(self, vm_id, region=None):
        if region:
            cs = self.pyrax.connect_to_cloudservers(region=region)
        else:
            cs = self.pyrax.cloudservers

        for server in cs.list():
            item = to_server_dict(server=server)
            if server.id == vm_id:
                return item

        return None
