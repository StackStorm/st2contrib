from st2actions.runners.pythonrunner import Action
import base64
import requests


class BaseAction(Action):
    def __init__(self, config):
        super(BaseAction, self).__init__(config)

        self._cmaddress = self.config.get('api_url')
        self._username = self.config.get('username')
        self._password = self.config.get('password')
        self._api_root = '/'.join([self._cmaddress, 'wsapis' 'v1.0.0'])
        self._headers = self._get_auth_token()

    def _get_auth_token(self):
        if not self._cmaddress or not self._username or not self._password:
            raise ValueError('Must define: "api_url", "username", and \
                              "password" config options')

        url = "/".join([self._cmaddress, self._api_root, 'auth', 'login'])
        auth_header = base64.b64encode('{}:{}'.format(self._username,
                                                      self._password))
        headers = {
            'Authorization': 'Basic {}'.format(auth_header)
        }

        r = requests.post(url, headers=headers)
        r.raise_for_status()
        headers = {
            'X-FeClient-Token': r.headers['X-FeClient-Token'],
            'X-FeApi-Token': r.headers['X-FeApi-Token'],
        }
        return headers

    def _api_get(self, endpoint, params=None):
        url = "/".join([self._api_root, endpoint])
        r = requests.get(url=url, params=params, headers=self._headers)
        r.raise_for_status()
        return r.text

    def _api_post(self, endpoint, files=None):
        url = "/".join([self._api_root, endpoint])
        r = requests.post(url=url, headers=self._headers, files=files)
        r.raise_for_status()
        return r.to_json()
