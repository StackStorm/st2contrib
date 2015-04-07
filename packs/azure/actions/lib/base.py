from st2actions.runners.pythonrunner import Action

from libcloud.compute.providers import Provider
from libcloud.compute.providers import get_driver

__all__ = [
    'AzureBaseAction'
]


class AzureBaseAction(Action):
    def __init__(self, config):
        super(AzureBaseAction, self).__init__(config=config)

        subscription_id = self.config['subscription_id']
        key_file = self.config['cert_file']
        self._driver = self._get_driver(subscription_id=subscription_id,
                                        key_file=key_file)

    def _get_driver(self, subscription_id, key_file):
        cls = get_driver(Provider.AZURE)
        driver = cls(subscription_id=subscription_id, key_file=key_file)
        return driver
