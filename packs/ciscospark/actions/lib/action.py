try:
    from ciscosparkapi import CiscoSparkAPI, DEFAULT_BASE_URL
except ImportError:
    message = ('Missing "ciscosparkapi", please install it using pip:\n'
               'pip install ciscosparkapi')
    raise ImportError(message)

from .ciscospark_parsers import CiscoSparkResultSets
from st2actions.runners.pythonrunner import Action

__all__ = [
    'CiscoSparkAction',
]


class CiscoSparkAction(Action):
    def __init__(self, config):
        super(CiscoSparkAction, self).__init__(config)
        self._access_token = self.config['access_token']
        self._base_url = self.config.get('base_url', DEFAULT_BASE_URL)
        self.connect()
        self._parser = CiscoSparkResultSets()

    def connect(self):
        self.connection = CiscoSparkAPI(access_token=self._access_token,
                                        base_url=self._base_url)

    def _parse_result(self, result):
        return self._parser.formatter(result)
