from lib.action import PyraxBaseAction

__all__ = [
    'DeleteNodeFromLoadBalancerAction'
]


class DeleteNodeFromLoadBalancerAction(PyraxBaseAction):
    def run(self, loadbalancer_id, ip):
        clb = self.pyrax.cloud_loadbalancers

        self.logger.info('Deleting node from loadbalancer...')

        load_balancer = clb.get(loadbalancer_id)
        target_ip = [node for node in load_balancer.nodes if node.address == ip][0]

        target_ip.delete()

        # Block until added
        self.pyrax.utils.wait_until(load_balancer, "status", "ACTIVE",
                                    interval=1, attempts=30, verbose=True)

        self.logger.info('Successfully removed node from loadbalancer: %s' % target_ip)

        return target_ip
