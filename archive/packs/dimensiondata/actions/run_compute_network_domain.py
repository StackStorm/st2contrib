from lib import actions

__all__ = [
    'ComputeNetworkDomainAction',
]


class ComputeNetworkDomainAction(actions.BaseAction):

    def run(self, **kwargs):
        network_domain_id = kwargs['network_domain_id']
        del kwargs['network_domain_id']
        action = kwargs['action']
        del kwargs['action']
        region = kwargs['region']
        del kwargs['region']
        driver = self._get_compute_driver(region)
        network_domain = driver.ex_get_network_domain(network_domain_id)
        kwargs['network_domain'] = network_domain
        return self._do_function(driver, action, **kwargs)
