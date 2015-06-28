from lib.action import PyraxBaseAction

__all__ = [
    'DeleteLoadBalancerAction'
]


class DeleteLoadBalancerAction(PyraxBaseAction):
    def run(self, loadbalancer_id):
        clb = self.pyrax.cloud_loadbalancers
        loadbalancer = clb.get(loadbalancer_id)

        loadbalancer.delete()
        return True
