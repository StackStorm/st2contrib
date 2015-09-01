from lib.actions import BaseAction

__all__ = [
    'ListBalancersAction'
]

RECORD_ATTRIBUTES = [
    'id',
    'name',
    'state',
    'ip',
    'port',
    'extra'
]


class ListBalancersAction(BaseAction):
    api_type = 'loadbalancer'

    def run(self, credentials):
        driver = self._get_driver_for_credentials(credentials=credentials)
        members = driver.list_balancers()
        result = []

        for record in members:
            values = record.__dict__
            item = dict([(k, v) for k, v in values.items()
                         if k in RECORD_ATTRIBUTES])
            result.append(item)

        return result
