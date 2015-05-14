from st2actions.runners.pythonrunner import Action
from st2client.client import Client
from st2client.models.datastore import KeyValuePair

__all__ = [
    'St2BaseAction'
]

class St2BaseAction(Action):
    def __init__(self, config):
        super(St2BaseAction, self).__init__(config)
        self._client = Client
        self._kvp = KeyValuePair
        self.client = self._get_client()

    def _get_client(self):
        host = self.config['base_url']

        try:
            return self._client(base_url=host)
        except Exception as e:
            return e
