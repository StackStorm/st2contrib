from lib.action import PyraxBaseAction
from lib.formatters import to_dns_record_dict

__all__ = [
    'CreateDNSRecordAction'
]


class CreateDNSRecordAction(PyraxBaseAction):
    def run(self, zone_id, name, type, data, priority=None, ttl=None,
            comment=None):
        cdns = self.pyrax.cloud_dns

        zone = cdns.get(zone_id)
        record_dict = {'name': name, 'type': type, 'data': data}

        if priority:
            record_dict['priority'] = priority

        if ttl:
            record_dict['ttl'] = ttl

        if comment:
            record_dict['comment'] = comment

        records = zone.add_records(records=[record_dict])

        result = to_dns_record_dict(records[0])
        return result
