from lib.actions import BaseAction

__all__ = [
    'ListVMsAction'
]


class ListVMsAction(BaseAction):
    api_type = 'compute'

    def run(self, credentials):
        driver = self._get_driver_for_credentials(credentials=credentials)
        vms = driver.list_nodes()

        return self.resultsets.formatter(vms)
