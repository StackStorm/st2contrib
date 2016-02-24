from libcloud.loadbalancer.base import Member

from lib.actions import BaseAction

__all__ = [
    'BalancerAttachMemberAction'
]


class BalancerAttachMemberAction(BaseAction):
    api_type = 'loadbalancer'

    def run(self, region, member_id, balancer_id, member_ip, member_port):
        driver = self._get_lb_driver(region)
        balancer = driver.get_balancer(balancer_id)
        member = Member(id=member_id, ip=member_ip, port=member_port)
        record = driver.balancer_attach_member(balancer=balancer,
                                               member=member)
        return self.resultsets.formatter(record)
