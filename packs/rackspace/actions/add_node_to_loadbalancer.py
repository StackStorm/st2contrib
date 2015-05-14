from lib.action import PyraxBaseAction

__all__ = [
    'AddNodeToLoadBalancerAction'
]


class AddNodeToLoadBalancerAction(PyraxBaseAction):
    def run(self, loadbalancer_id, ip, port):
        clb = self.pyrax.cloud_loadbalancers
        node = clb.Node(address=ip, port=port, condition="ENABLED")

        self.logger.info('Adding node to loadbalancer...')

        load_balancer = clb.get(loadbalancer_id)
        load_balancer.add_nodes(node)

        # Block until added
        self.pyrax.utils.wait_until(load_balancer, "status", "ACTIVE",
                                    interval=1, attempts=30, verbose=True)

        self.logger.info('Successfully added node to loadbalancer: %s' % node)

        return node
