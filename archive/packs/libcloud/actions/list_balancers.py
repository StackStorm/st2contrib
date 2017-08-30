from lib.actions import BaseAction

__all__ = [
    'ListBalancersAction'
]


class ListBalancersAction(BaseAction):
    api_type = 'loadbalancer'

    def run(self, credentials):
        driver = self._get_driver_for_credentials(credentials=credentials)
        members = driver.list_balancers()
        return self.resultsets.formatter(members)
