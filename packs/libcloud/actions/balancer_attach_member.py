from libcloud.loadbalancer.base import Member

from lib.actions import BaseAction

__all__ = [
    'BalancerAttachMemberAction'
]

RECORD_ATTRIBUTES = [
    'id'
]


class BalancerAttachMemberAction(BaseAction):
    api_type = 'loadbalancer'

    def run(self, credentials, balancer_id, member_ip, member_port):
        driver = self._get_driver_for_credentials(credentials=credentials)
        balancer = driver.get_balancer(balancer_id)
        member = Member(id=None, ip=member_ip, port=member_port)
        record = driver.balancer_attach_member(balancer=balancer,
                                               member=member)
        result = []

        values = record.__dict__
        item = dict([(k, v) for k, v in values.items()
                     if k in RECORD_ATTRIBUTES])
        result.append(item)

        return result
