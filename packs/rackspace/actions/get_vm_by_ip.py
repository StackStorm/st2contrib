from lib.action import BaseVMsAction
from lib.formatters import to_server_dict

__all__ = [
    'GetVMByIP'
]


class GetVMByIP(BaseVMsAction):
    def run(self, ip_address, region=None):
        if region:
            cs = self.pyrax.connect_to_cloudservers(region=region)
        else:
            cs = self.pyrax.cloudservers

        servers = cs.list()

        result = None
        for server in servers:
            item = to_server_dict(server=server)
            public_ips = item.get('public_ips', [])

            if ip_address in public_ips:
                result = item
                break

        return result
