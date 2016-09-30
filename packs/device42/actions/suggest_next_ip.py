from lib.base_action import BaseAction


class SuggestNextIp(BaseAction):
    def run(self, subnet_id=None, subnet=None, name=None, vrf_group_id=None, vrf_group=None,
            reserved_ip=None):
        response = self.getAPI("/api/1.0/suggest_ip/", {
            "subnet_id": subnet_id,
            "subnet": subnet,
            "name": name,
            "vrf_group_id": vrf_group_id,
            "vrf_group": vrf_group,
            "reserved_ip": reserved_ip,
        })

        return response["ip"]
