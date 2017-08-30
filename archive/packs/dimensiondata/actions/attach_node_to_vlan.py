from lib import actions

__all__ = [
    'AttachNodeToVlanAction',
]


class AttachNodeToVlanAction(actions.BaseAction):

    def run(self, **kwargs):
        node_id = kwargs['node_id']
        del kwargs['node_id']
        action = kwargs['action']
        del kwargs['action']
        region = kwargs['region']
        del kwargs['region']
        vlan_id = kwargs['vlan_id']
        del kwargs['vlan_id']
        driver = self._get_compute_driver(region)
        node = driver.ex_get_node_by_id(node_id)
        vlan = driver.ex_get_vlan(vlan_id)
        kwargs['node'] = node
        kwargs['vlan'] = vlan
        return self._do_function(driver, action, **kwargs)
