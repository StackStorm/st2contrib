from lib.action import PyraxBaseAction

__all__ = [
    'FindDNSRecordIdAction'
]


class FindDNSRecordIdAction(PyraxBaseAction):
    def run(self, name, zone_id):
        cdns = self.pyrax.cloud_dns
        dns_id = [record for record in cdns.list_records(zone_id)
                 if record.name == name][0].id

        return dns_id
