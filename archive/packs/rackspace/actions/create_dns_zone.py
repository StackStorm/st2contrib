from lib.action import PyraxBaseAction
from lib.formatters import to_dns_zone_dict

__all__ = [
    'CreateDNSZoneAction'
]


class CreateDNSZoneAction(PyraxBaseAction):
    def run(self, name, email_address, ttl=None, comment=None):
        cdns = self.pyrax.cloud_dns

        zone = cdns.create(name=name, emailAddress=email_address, ttl=ttl,
                           comment=comment)
        result = to_dns_zone_dict(zone)
        return result
