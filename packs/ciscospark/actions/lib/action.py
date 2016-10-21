try:
    from ciscosparkapi import CiscoSparkAPI
except ImportError:
    message = ('Missing "ciscosparkapi", please install it using pip:\n'
               'pip install ciscosparkapi')
    raise ImportError(message)

from st2actions.runners.pythonrunner import Action

__all__ = [
    'CiscoSparkAction',
]


class CiscoSparkAction(Action):
    def __init__(self, config):
        super(CiscoSparkAction, self).__init__(config)
        self._access_token = self.config['access_token']
        self._base_url = self.config['base_url']
        self.connect()

    def connect(self):
        self.connection = CiscoSparkAPI(access_token=self._access_token,
                                        base_url=self._base_url)
