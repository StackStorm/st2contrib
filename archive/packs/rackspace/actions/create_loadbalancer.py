from lib.action import PyraxBaseAction

__all__ = [
    'CreateLoadBalancerAction'
]


class CreateLoadBalancerAction(PyraxBaseAction):
    def run(self, name, port, protocol):
        clb = self.pyrax.cloud_loadbalancers
        virtual_ipv4 = clb.VirtualIP(type="PUBLIC", ipVersion='IPV4')

        self.logger.info('Creating loadbalancer...')

        load_balancer = clb.create(name, port=port, protocol=protocol, virtual_ips=[virtual_ipv4])

        # Block until provisioned
        self.pyrax.utils.wait_until(load_balancer, "status", "ACTIVE", interval=1,
                                    attempts=30)

        self.logger.info('Loadbalancer successfully created: %s' % load_balancer)

        payload = {
            'cluster': load_balancer.cluster,
            'algorithm': load_balancer.algorithm,
            'id': load_balancer.id,
            'name': load_balancer.name,
            'port': load_balancer.port,
            'protocol': load_balancer.protocol,
            'ipv4_public': load_balancer.sourceAddresses['ipv4Public'],
            'ipv4_service': load_balancer.sourceAddresses['ipv4Servicenet'],
            'ipv6_public': load_balancer.sourceAddresses['ipv6Public'],
            'logging': load_balancer.connectionLogging['enabled'],
            'caching': load_balancer.contentCaching['enabled'],
            'https_redirect': load_balancer.httpsRedirect,
            'timeout': load_balancer.timeout,
            'status': load_balancer.status
        }

        return payload
