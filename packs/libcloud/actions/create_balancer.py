from lib.actions import BaseAction

__all__ = [
    'CreateBalancerAction'
]

RECORD_ATTRIBUTES = [
    'id'
]


class CreateBalancerAction(BaseAction):
    api_type = 'loadbalancer'

    def run(self, credentials, name, port, protocol):
        driver = self._get_driver_for_credentials(credentials=credentials)
        record = driver.create_balancer(name=name,
                                        port=port,
                                        protocol=protocol)

        result = []

        values = record.__dict__
        item = dict([(k, v) for k, v in values.items()
                     if k in RECORD_ATTRIBUTES])
        result.append(item)

        return result
