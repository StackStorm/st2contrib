import httplib

import requests

from st2actions.runners.pythonrunner import Action

BASE_API_URL = 'https://circleci.com/api'
API_VERSION = 'v1'
API_URL = '%s/%s/' % (BASE_API_URL, API_VERSION)
HEADER_ACCEPT = 'application/json'
HEADER_CONTENT_TYPE = 'application/json'


class CircleCI(Action):
    def _get_base_headers(self):
        headers = {}
        headers['Content-Type'] = HEADER_CONTENT_TYPE
        headers['Accept'] = HEADER_ACCEPT
        return headers

    def _get_auth_headers(self):
        headers = self._get_base_headers()
        token = self.config.get('token', None)

        if not token:
            raise Exception('Token not found in config file.')

        headers['circle-token'] = token
        return headers

    def _perform_request(self, path, method, data=None, requires_auth=True,
                         extra_headers=None):
        url = API_URL + path

        headers = self._get_base_headers()
        if requires_auth:
            headers = self._get_auth_headers()

        if extra_headers:
            headers.update(extra_headers)

        if method == "GET":
            response = requests.get(url, headers=headers)
        elif method == 'POST':
            response = requests.post(url, headers=headers)
        elif method == 'PUT':
            response = requests.put(url, data=data, headers=headers)

        if response.status_code in [httplib.FORBIDDEN, httplib.UNAUTHORIZED]:
            msg = ('Invalid or missing Travis CI auth token. ' +
                   'Make sure you have'
                   'specified valid token in the config file')
            raise Exception(msg)

        return response
