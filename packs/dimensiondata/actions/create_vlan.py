from lib import actions

__all__ = [
    'CreateVlanAction',
]


class CreateVlanAction(actions.BaseAction):

    def run(self, **kwargs):
        action = kwargs['action']
        del kwargs['action']
        region = kwargs['region']
        del kwargs['region']
        network_domain_id = kwargs['network_domain_id']
        del kwargs['network_domain_id']
        driver = self._get_compute_driver(region)
        network_domain = driver.ex_get_network_domain(network_domain_id)
        kwargs['network_domain'] = network_domain
        result = self._do_function(driver, action, **kwargs)
        # Wait to complete
        driver.ex_wait_for_state('NORMAL', driver.ex_get_vlan,
                                 poll_interval=2, timeout=1200,
                                 vlan_id=result['id'])
        return result
