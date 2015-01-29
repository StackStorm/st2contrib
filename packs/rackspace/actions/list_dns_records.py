from lib.action import PyraxBaseAction
from lib.formatters import to_dns_record_dict

__all__ = [
    'ListDNSRecordsAction'
]


class ListDNSRecordsAction(PyraxBaseAction):
    def run(self, zone_id):
        cdns = self.pyrax.cloud_dns
        zone = cdns.get(zone_id)
        records = zone.list_records()

        result = []
        for record in records:
            item = to_dns_record_dict(record=record)
            result.append(item)

        return result
