from lib.action import PyraxBaseAction

__all__ = [
    'DeleteDNSZoneAction'
]


class DeleteDNSZoneAction(PyraxBaseAction):
    def run(self, zone_id):
        cdns = self.pyrax.cloud_dns
        zone = cdns.get(zone_id)

        zone.delete()
        return True
