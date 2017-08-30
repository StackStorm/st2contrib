from lib.actions import BaseAction

__all__ = [
    'BalancerDetachMemberAction'
]


class BalancerDetachMemberAction(BaseAction):
    api_type = 'loadbalancer'

    def run(self, region, balancer_id, member_id):
        driver = self._get_lb_driver(region)
        balancer = driver.get_balancer(balancer_id)
        member = driver.ex_get_pool_member(member_id)
        record = driver.balancer_detach_member(balancer=balancer,
                                               member=member)
        return self.resultsets.formatter(record)
