from lib.actions import BaseAction

__all__ = [
    'ListDNSZonesAction'
]


class ListDNSZonesAction(BaseAction):
    api_type = 'dns'

    def run(self, credentials):
        driver = self._get_driver_for_credentials(credentials=credentials)
        zones = driver.list_zones()
        return self.resultsets.formatter(zones)
