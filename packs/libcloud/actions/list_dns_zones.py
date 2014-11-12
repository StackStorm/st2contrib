from lib.actions import BaseAction

__all__ = [
    'ListDNSZonesAction'
]

ZONE_ATTRIBUTES = [
    'id',
    'domain',
    'type',
    'ttl'
]


class ListDNSZonesAction(BaseAction):
    def run(self, credentials):
        driver = self._get_driver_for_credentials(credentials=credentials)
        zones = driver.list_zones()
        result = []

        for zone in zones:
            values = zone.__dict__
            item = dict([(k, v) for k, v in values.items()
                         if k in ZONE_ATTRIBUTES])
            result.append(item)

        return result
