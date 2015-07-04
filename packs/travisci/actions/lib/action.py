import requests

from st2actions.runners.pythonrunner import Action

API_URL = 'https://api.travis-ci.org'
HEADERS_ACCEPT = 'application/vnd.travis-ci.2+json'
HEADERS_HOST = ''


class TravisCI(Action):
    def __init__(self, config):
        super(TravisCI, self).__init__(config)

    def _get_auth_headers(self):
        headers = {}
        headers['Authorization'] = self.config["Authorization"]
        headers['Content-Type'] = self.config["Content-Type"]
        return headers

    def _perform_request(self, uri, method, data=None, requires_auth=False):
        if method == "GET":
            if requires_auth:
                headers = self._get_auth_headers()
            else:
                headers = {}
            response = requests.get(uri, headers=headers)
        elif method == 'POST':
            headers = self._get_auth_headers()
            response = requests.post(uri, headers=headers)
        elif method == 'PUT':
            headers = self._get_auth_headers()
            response = requests.put(uri, data=data, headers=headers)
        return response
