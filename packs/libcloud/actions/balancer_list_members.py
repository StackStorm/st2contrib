from libcloud.loadbalancer.base import LoadBalancer

from lib.actions import BaseAction

__all__ = [
    'BalancerListMembersAction'
]

RECORD_ATTRIBUTES = [
    'id',
    'ip',
    'port',
    'extra',
]


class BalancerListMembersAction(BaseAction):
    api_type = 'loadbalancer'

    def run(self, credentials, balancer_id):
        driver = self._get_driver_for_credentials(credentials=credentials)
        balancer = driver.get_balancer(balancer_id)
        members = driver.balancer_list_members(balancer=balancer)
        result = []

        for record in members:
            values = record.__dict__
            item = dict([(k, v) for k, v in values.items()
                         if k in RECORD_ATTRIBUTES])
            result.append(item)

        return result
