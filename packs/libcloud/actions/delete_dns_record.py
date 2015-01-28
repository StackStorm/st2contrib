from libcloud.dns.base import Record
from libcloud.dns.base import Zone

from lib.actions import BaseAction

__all__ = [
    'DeleteDNSRecordAction'
]


class DeleteDNSRecordAction(BaseAction):
    api_type = 'dns'

    def run(self, credentials, zone_id, record_id):
        driver = self._get_driver_for_credentials(credentials=credentials)
        zone = Zone(id=zone_id, domain=None, type=None, ttl=None, driver=driver)
        record = Record(id=record_id, name=None, type=None, data=None,
                        zone=zone, driver=driver)

        status = driver.delete_record(record=record)

        if status:
            self.logger.info('Successfully deleted record')
        else:
            self.logger.error('Failed to delete a record')

        return status
