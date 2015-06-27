from libcloud.compute.providers import Provider
from libcloud.compute.providers import get_driver
from st2actions.runners.pythonrunner import Action


class SoftlayerBaseAction(Action):
    def __init__(self, config):
        # Handy translation from our parameters to libcloud ones
        self.st2_to_libcloud = {
            "domain": "ex_domain",
            "os": "ex_os",
            "ram": "ex_ram",
            "disk": "ex_disk",
            "cpus": "ex_cpus",
            "bandwith": "ex_bandwidth",
            "local_disk": "ex_local_disk",
            "datacenter": "ex_datacenter",
            "keyname": "ex_keyname"
        }
        super(SoftlayerBaseAction, self).__init__(config=config)

    def _get_driver(self):
        cls = get_driver(Provider.SOFTLAYER)
        return cls(self.config['username'], self.config['api_key'])
