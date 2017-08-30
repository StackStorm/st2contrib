from analysis_apiclient import AnalysisClient  # noqa
from st2actions.runners.pythonrunner import Action


class BaseAction(Action):
    def __init__(self, config):
        super(BaseAction, self).__init__(config)

        self._url = self.config.get('url', 'https://analysis.lastline.com')
        self._key = self.config.get('key')
        self._api_token = self.config.get('api_token')

        self.client = self._init_client()

    def _init_client(self):
        if not self._key:
            raise ValueError('Missing "key" config option')
        if not self._api_token:
            raise ValueError('Missing "api_token" config option')

        return AnalysisClient(self._url, self._key, self._api_token)  # noqa
