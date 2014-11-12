from libcloud.dns.base import Zone

from lib.actions import BaseAction

__all__ = [
    'ListDNSRecordsAction'
]

RECORD_ATTRIBUTES = [
    'id',
    'name',
    'type',
    'data',
]


class ListDNSRecordsAction(BaseAction):
    def run(self, credentials, zone_id):
        driver = self._get_driver_for_credentials(credentials=credentials)
        zone = Zone(id=zone_id, domain=None, type=None, ttl=None, driver=None)
        records = driver.list_records(zone=zone)
        result = []

        for record in records:
            values = record.__dict__
            item = dict([(k, v) for k, v in values.items()
                         if k in RECORD_ATTRIBUTES])
            result.append(item)

        return result
