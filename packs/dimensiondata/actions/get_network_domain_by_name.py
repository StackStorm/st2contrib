from lib import actions

__all__ = [
    'GetNetworkDomainByNameAction',
]


class GetNetworkDomainByNameAction(actions.BaseAction):

    def run(self, region, network_domain_name):
        driver = self._get_compute_driver(region)
        networkdomains = driver.ex_list_network_domains()
        networkdomain = list(filter(lambda x: x.name == network_domain_name,
                                    networkdomains))[0]
        return self.resultsets.formatter(networkdomain)
