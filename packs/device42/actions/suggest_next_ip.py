from st2actions.runners.pythonrunner import Action
import requests


class SuggestNextIp(Action):
    def run(self, subnet_id=None, subnet=None, name=None, vrf_group_id=None, vrf_group=None,
            reserved_ip=None):
        d42_server = self.config.get('d42_server', None)
        if not d42_server:
            raise ValueError('"d42_server" config value is required')

        d42_username = self.config.get('d42_username', None)
        if not d42_username:
            raise ValueError('"d42_username" config value is required')

        d42_password = self.config.get('d42_password', None)
        if not d42_password:
            raise ValueError('"d42_password" config value is required')

        protocol = self.config.get('protocol', 'http')

        verify = False
        if self.confing.get('verify_certificate', None) == 'true' and protocol == 'https':
            verify = True

        if not subnet_id and not subnet and not name:
            raise ValueError('"subnet_id" or "subnet" or "name" value is required')

        response = requests.get("%s://%s%s" % (protocol, d42_server, "/api/1.0/suggest_ip/"), params={
            "subnet_id": subnet_id,
            "subnet": subnet,
            "name": name,
            "vrf_group_id": vrf_group_id,
            "vrf_group": vrf_group,
            "reserved_ip": reserved_ip,
        }, auth=(d42_username, d42_password), verify=verify)

        return response.json()["ip"]
