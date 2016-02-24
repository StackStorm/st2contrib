from lib import actions

__all__ = [
    'DeleteVlanAction',
]


class DeleteVlanAction(actions.BaseAction):

    def run(self, **kwargs):
        action = kwargs['action']
        del kwargs['action']
        region = kwargs['region']
        del kwargs['region']
        vlan_id = kwargs['vlan_id']
        del kwargs['vlan_id']
        driver = self._get_compute_driver(region)
        vlan = driver.ex_get_vlan(vlan_id)
        kwargs['vlan'] = vlan
        return self._do_function(driver, action, **kwargs)
