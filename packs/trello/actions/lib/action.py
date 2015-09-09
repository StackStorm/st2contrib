from trello import TrelloClient

from st2actions.runners.pythonrunner import Action


class BaseAction(Action):
    def __init__(self, config):
        super(BaseAction, self).__init__(config)
        self._load_default_creds()
        self.client = None

    def _load_default_creds(self):
        self._creds = {}
        self._creds['api_key'] = self.config['api_key']

        if self.config['token']:
            self._creds['token'] = self.config['token']
        else:
            self._creds['token'] = None

    def _set_creds(self, api_key, token=None):
        self._creds = {
            'api_key': api_key,
            'token': token,
        }

    def _client(self):
        if not self.client:
            self.client = TrelloClient(api_key=self._creds['api_key'],
                                       token=self._creds['token'])

        return self.client
