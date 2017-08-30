from libcloud.dns.base import Zone

from lib.actions import BaseAction

__all__ = [
    'ListDNSRecordsAction'
]


class ListDNSRecordsAction(BaseAction):
    api_type = 'dns'

    def run(self, credentials, zone_id):
        driver = self._get_driver_for_credentials(credentials=credentials)
        zone = Zone(id=zone_id, domain=None, type=None, ttl=None, driver=None)
        records = driver.list_records(zone=zone)
        return self.resultsets.formatter(records)
