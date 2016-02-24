from libcloud.loadbalancer.base import Algorithm

from lib.actions import BaseAction

__all__ = [
    'CreateBalancerAction'
]


class CreateBalancerAction(BaseAction):

    def run(self, region, network_domain_id, name, port, protocol,
            algorithm=Algorithm.ROUND_ROBIN):
        driver = self._get_lb_driver(region)

        # Use a local lookup - these maps are protected fields of each driver
        _VALUE_TO_ALGORITHM_MAP = {
            'ROUND_ROBIN': Algorithm.ROUND_ROBIN,
            'LEAST_CONNECTIONS': Algorithm.LEAST_CONNECTIONS,
            'SHORTEST_RESPONSE': Algorithm.SHORTEST_RESPONSE,
            'PERSISTENT_IP': Algorithm.PERSISTENT_IP
        }

        if algorithm is not Algorithm.ROUND_ROBIN:
            algorithm = _VALUE_TO_ALGORITHM_MAP[algorithm]
        driver.network_domain_id = network_domain_id
        record = driver.create_balancer(name=name,
                                        port=port,
                                        protocol=protocol,
                                        algorithm=algorithm,
                                        members=None)

        return self.resultsets.formatter(record)
