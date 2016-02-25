from lib import actions

__all__ = [
    'GetVMByNameAction',
]


class GetVMByNameAction(actions.BaseAction):

    def run(self, region, location, name, network_domain):
        driver = self._get_compute_driver(region)

        if network_domain is not None:
            networkdomains = driver.ex_list_network_domains()
            network_domain = list(filter(lambda x: x.name == network_domain,
                                         networkdomains))[0]
            nodes = driver.list_nodes(ex_network_domain=network_domain)
        else:
            nodes = driver.list_nodes()
        node = list(filter(lambda x: x.name == name, nodes))[0]
        return self.resultsets.formatter(node)
