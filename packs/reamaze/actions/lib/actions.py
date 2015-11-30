from st2actions.runners.pythonrunner import Action
import requests


class BaseAction(Action):
    def __init__(self, config):
        super(BaseAction, self).__init__(config)

        self._email    = self.config.get('email')
        self._token    = self.config.get('api_token')
        self._api_root = '/api/v1'
        self._headers  = {'Accept': 'application/json'}

    def _api_get(self, endpoint, headers={}, params=None):
        _url = self._api_root + endpoint
        _headers = self._headers.update(headers)

        r = requests.get(url=_url, auth=(self._email, self._token),
                         params=params, headers=_headers)

        r.raise_for_status()
        return r.json()
