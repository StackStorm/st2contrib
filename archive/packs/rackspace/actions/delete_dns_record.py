from lib.action import PyraxBaseAction

__all__ = [
    'DeleteDNSRecordAction'
]


class DeleteDNSRecordAction(PyraxBaseAction):
    def run(self, zone_id, record_id):
        cdns = self.pyrax.cloud_dns
        zone = cdns.get(zone_id)
        record = zone.get_record(record_id)

        record.delete()
        return True
