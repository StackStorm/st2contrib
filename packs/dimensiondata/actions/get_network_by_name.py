from lib import actions

__all__ = [
    'GetNetworkByNameAction',
]


class GetNetworkByNameAction(actions.BaseAction):

    def run(self, region, network_name):
        driver = self._get_compute_driver(region)
        networks = driver.ex_list_networks()
        network = list(filter(lambda x: x.name == network_name,
                            networks))[0]
        return self.resultsets.formatter(network)
