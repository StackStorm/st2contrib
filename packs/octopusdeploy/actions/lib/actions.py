try:
    import requests
except ImportError:
    message = ('Missing "requests", please install it using pip:\n'
               'pip install requests')
    raise ImportError(message)

try:
    import json
except ImportError:
    message = ('Missing "json", please install it using pip:\n'
               'pip install requests')
    raise ImportError(message)

from st2actions.runners.pythonrunner import Action

__all__ = [
    'OctopusDeployAction',
]


class OctopusDeployAction(Action):
    def __init__(self, config):
        super(OctopusDeployAction, self).__init__(config)
        self.client = self._init_client()

    def _init_client(self):
        api_key = self.config['api_key']
        host = self.config['host']
        port = self.config['port']
        return OctopusDeployClient(api_key=api_key, host=host, port=port)

    def _build_uri(self):
        # big assumption but it'll cover 99% case,
        # as octopus runs https by default
        start = "http://" if self.client.port is 80 else "https://"
        return start + self.client.host + ":" + str(self.client.port) + "/api/"

    def make_post_request(self, action, payload):
        response = requests.post(self._build_uri() + action,
                                 data=json.dumps(payload), verify=False,
                                 headers=self.client.headers)
        return response.json()

    def make_get_request(self, action):
        response = requests.get(self._build_uri() + action,
                                verify=False,
                                headers=self.client.headers)
        return response.json()


class OctopusDeployClient(object):
    def __init__(self, api_key, host, port):
        self.api_key = api_key
        self.host = host
        self.port = port
        self.headers = {'X-Octopus-ApiKey': self.api_key,
                        'Content-type': 'application/json',
                        'Accept': 'text/plain'}
