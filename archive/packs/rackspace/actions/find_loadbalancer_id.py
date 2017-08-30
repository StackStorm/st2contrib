from lib.action import PyraxBaseAction

__all__ = [
    'FindLoadBalancerIdAction'
]


class FindLoadBalancerIdAction(PyraxBaseAction):
    def run(self, name):
        clb = self.pyrax.cloud_loadbalancers
        lb_id = [lb for lb in clb.list()
                 if lb.name == name][0].id

        return lb_id
