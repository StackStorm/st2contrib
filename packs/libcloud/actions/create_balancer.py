from libcloud.loadbalancer.base import Algorithm

from lib.actions import BaseAction

__all__ = [
    'CreateBalancerAction'
]

RECORD_ATTRIBUTES = [
    'id'
]


class CreateBalancerAction(BaseAction):
    api_type = 'loadbalancer'

    def run(self, credentials, name, port, protocol,
            algorithm=Algorithm.ROUND_ROBIN):
        driver = self._get_driver_for_credentials(credentials=credentials)

        # Use a local lookup - these maps are protected fields of each driver
        _VALUE_TO_ALGORITHM_MAP = {
            'ROUND_ROBIN': Algorithm.ROUND_ROBIN,
            'LEAST_CONNECTIONS': Algorithm.LEAST_CONNECTIONS,
            'SHORTEST_RESPONSE': Algorithm.SHORTEST_RESPONSE,
            'PERSISTENT_IP': Algorithm.PERSISTENT_IP
        }

        if algorithm is not Algorithm.ROUND_ROBIN:
            algorithm = _VALUE_TO_ALGORITHM_MAP[algorithm]

        record = driver.create_balancer(name=name,
                                        port=port,
                                        protocol=protocol,
                                        algorithm=algorithm,
                                        members=None)

        result = []

        values = record.__dict__
        item = dict([(k, v) for k, v in values.items()
                     if k in RECORD_ATTRIBUTES])
        result.append(item)

        return result
