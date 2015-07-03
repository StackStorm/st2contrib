from st2actions.runners.pythonrunner import Action
import requests

class TravisCI(Action):
    def __init__(self, config):
        super(TravisCI, self).__init__(config)

    def _init_header(self):
        travis_header = {
                  'User_Agent': self.config['User-Agent'],
                  'Accept': self.config['Accept'],
                  'Host': self.config['Host'],
        }
        return travis_header
    
    def _auth_header(self):
        _HEADERS = self._init_header()
        _HEADERS['Authorization'] = self.config["Authorization"]
        _HEADERS['Content-Type'] = self.config["Content-Type"]
        return _HEADERS
    
    def _perform_request(self, uri, method, data=None, requires_auth=False):
        if method == "GET":
            if requires_auth:
                _HEADERS = self._auth_header()
            else:
                _HEADERS = self._init_header()
            response = requests.get(uri, headers=_HEADERS)
        elif method == "POST":
            _HEADERS = self._auth_header
            response = requests.post(uri, headers=_HEADERS)
        elif method == "PUT":
            _HEADERS = self._auth_header()
            _HEADERS['Authorization'] = self.config["Authorization"]
            _HEADERS['Content-Type'] = self.config["Content-Type"]
            response = requests.put(uri, data=data, headers=_HEADERS)
        return response
