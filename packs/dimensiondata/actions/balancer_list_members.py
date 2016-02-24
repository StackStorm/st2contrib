from lib.actions import BaseAction

__all__ = [
    'BalancerListMembersAction'
]


class BalancerListMembersAction(BaseAction):

    def run(self, region, balancer_id):
        driver = self._get_lb_driver(region)
        balancer = driver.get_balancer(balancer_id)
        members = driver.balancer_list_members(balancer=balancer)
        return self.resultsets.formatter(members)
