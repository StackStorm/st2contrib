from st2actions.runners.pythonrunner import Action

from libcloud.compute.providers import Provider as ComputeProvider
from libcloud.compute.providers import get_driver as get_compute_driver
from libcloud.storage.providers import Provider as StorageProvider
from libcloud.storage.providers import get_driver as get_storage_driver

__all__ = [
    'AzureBaseComputeAction',
    'AzureBaseStorageAction'
]


class AzureBaseComputeAction(Action):
    def __init__(self, config):
        super(AzureBaseComputeAction, self).__init__(config=config)

        config = self.config['compute']
        subscription_id = config['subscription_id']
        key_file = config['cert_file']
        self._driver = self._get_driver(subscription_id=subscription_id,
                                        key_file=key_file)

    def _get_driver(self, subscription_id, key_file):
        cls = get_compute_driver(ComputeProvider.AZURE)
        driver = cls(subscription_id=subscription_id, key_file=key_file)
        return driver


class AzureBaseStorageAction(Action):
    def __init__(self, config):
        super(AzureBaseStorageAction, self).__init__(config=config)

        config = self.config['storage']
        name = config['name']
        access_key = config['access_key']
        self._driver = self._get_driver(name=name, access_key=access_key)

    def _get_driver(self, name, access_key):
        cls = get_storage_driver(StorageProvider.AZURE_BLOBS)
        driver = cls(key=name, secret=access_key)
        return driver
