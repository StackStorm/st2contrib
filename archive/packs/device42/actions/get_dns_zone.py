import dns.rdataset
import dns.zone

from lib.base_action import BaseAction


class GetDnsZone(BaseAction):
    def run(self, domain, record_type=None, name=None, nameserver=None, content=None, tags=None,
            tags_and=None):
        response = self.getAPI("/api/1.0/dns/records/", {
            "domain": domain,
            "type": record_type,
            "name": name,
            "nameserver": nameserver,
            "content": content,
            "tags": tags,
            "tags_and": tags_and
        })

        result = ""
        if len(response["records"]) > 0:
            zone = dns.zone.Zone(dns.name.from_text(response["records"][0]["dns_zone"]))
            for record in response["records"]:
                try:
                    rdtype = dns.rdatatype.from_text(record["type"])
                    rdata = dns.rdata.from_text(dns.rdataclass.IN, rdtype, record["content"])
                    n = zone.get_rdataset(record["name"], rdtype, create=True)
                    n.add(rdata, record["ttl"])
                except Exception, e:
                    print "Error: %s" % e.message
                    print "Record Name: %s" % record["name"]
                    print "Record Type: %s" % record["type"]
                    print "Record Content: %s" % record["content"]
                    print "Record TTL: %d" % record["ttl"]
                    print "---"
            result = zone.to_text()
        return result
