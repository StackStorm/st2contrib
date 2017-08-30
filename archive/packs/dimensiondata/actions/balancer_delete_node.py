from lib.actions import BaseAction

__all__ = [
    'BalancerDeleteNodeAction'
]


class BalancerDeleteNodeAction(BaseAction):
    api_type = 'loadbalancer'

    def run(self, region, node_id):
        driver = self._get_lb_driver(region)
        record = driver.ex_destroy_node(node_id)
        return self.resultsets.formatter(record)
