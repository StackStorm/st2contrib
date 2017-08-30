from lib import actions

__all__ = [
    'GetIPV6AddressAction',
]


class GetIPV6AddressAction(actions.BaseAction):

    def run(self, region, id):
        driver = self._get_compute_driver(region)
        node = driver.ex_get_node_by_id(id)
        return node.extra['ipv6']
