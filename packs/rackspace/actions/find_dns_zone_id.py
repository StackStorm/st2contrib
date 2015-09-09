from lib.action import PyraxBaseAction

__all__ = [
    'FindDNSIdAction'
]


class FindDNSIdAction(PyraxBaseAction):
    def run(self, name):
        cdns = self.pyrax.cloud_dns
        zone_id = [zone for zone in cdns.list()
                   if zone.name == name][0].id

        return zone_id
