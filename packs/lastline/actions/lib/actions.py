import analysis_apiclient
from st2actions.runners.pythonrunner import Action

class BaseAction(Action):
    def __init__(self, config):
        super(LastlineAction, self).__init__(config)
        self.client = self._init_client()

    def _init_client(self):
        url = config.get('url', 'https://analysis.lastline.com')
        key = config.get('key')
        api_token = config.get('api_token')

        if not key:
            return ValueError('Missing "key" config option')
        if not api_token:
            return ValueError('Missing "api_token" config option')

        return AnalysisClient(url, key, api_token)
