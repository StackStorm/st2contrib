import httplib

import requests

from st2actions.runners.pythonrunner import Action

API_URL = 'https://api.travis-ci.org'
HEADERS_ACCEPT = 'application/vnd.travis-ci.2+json'
CONTENT_TYPE = 'application/json'


class TravisCI(Action):
    def _get_auth_headers(self):
        headers = {}
        headers['Authorization'] = self.config['Authorization']
        headers['Content-Type'] = self.config['Content-Type']
        return headers

    def _perform_request(self, path, method, data=None, requires_auth=False):
        url = API_URL + path

        if method == "GET":
            if requires_auth:
                headers = self._get_auth_headers()
            else:
                headers = {}
            response = requests.get(url, headers=headers)
        elif method == 'POST':
            headers = self._get_auth_headers()
            response = requests.post(url, headers=headers)
        elif method == 'PUT':
            headers = self._get_auth_headers()
            response = requests.put(url, data=data, headers=headers)

        if response.status_code in [httplib.FORBIDDEN, httplib.UNAUTHORIZED]:
            msg = ('Invalid or missing Travis CI auth token. Make sure you have'
                   'specified valid token in the config file')
            raise Exception(msg)

        return response
