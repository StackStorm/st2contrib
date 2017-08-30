from lib.actions import BaseAction

__all__ = [
    'CreatePoolMemberAction'
]


class CreatePoolMemberAction(BaseAction):
    api_type = 'loadbalancer'

    def run(self, region, pool_id, node_id, port):
        driver = self._get_lb_driver(region)
        pool = driver.ex_get_pool(pool_id)
        node = driver.ex_get_node(node_id)
        member = driver.ex_create_pool_member(pool, node, port)
        return self.resultsets.formatter(member)
