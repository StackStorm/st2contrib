from lib import actions

__all__ = [
    'ComputeNodeAction',
]


class ComputeNodeAction(actions.BaseAction):

    def run(self, **kwargs):
        node_id = kwargs['node_id']
        del kwargs['node_id']
        action = kwargs['action']
        del kwargs['action']
        region = kwargs['region']
        del kwargs['region']
        driver = self._get_compute_driver(region)
        node = driver.ex_get_node_by_id(node_id)
        kwargs['node'] = node
        return self._do_function(driver, action, **kwargs)
