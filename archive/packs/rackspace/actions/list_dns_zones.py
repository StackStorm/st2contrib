from lib.action import PyraxBaseAction
from lib.formatters import to_dns_zone_dict

__all__ = [
    'ListDNSZonesAction'
]


class ListDNSZonesAction(PyraxBaseAction):
    def run(self):
        cdns = self.pyrax.cloud_dns
        zones = cdns.list()

        result = []
        for zone in zones:
            item = to_dns_zone_dict(zone=zone)
            result.append(item)

        return result
