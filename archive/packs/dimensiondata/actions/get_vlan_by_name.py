from lib import actions

__all__ = [
    'GetVLANByNameAction',
]


class GetVLANByNameAction(actions.BaseAction):

    def run(self, region, vlan_name, network_domain_id):
        driver = self._get_compute_driver(region)
        if network_domain_id is not None:
            network_domain = driver.ex_get_network_domain(network_domain_id)
            vlans = driver.ex_list_vlans(network_domain=network_domain)
        else:
            vlans = driver.ex_list_vlans()
        vlan = list(filter(lambda x: x.name == vlan_name,
                    vlans))[0]
        return self.resultsets.formatter(vlan)
