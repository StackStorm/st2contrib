import requests
import base64
from st2actions.runners.pythonrunner import Action


class BaseAction(Action):
    def __init__(self, config):
        super(BaseAction, self).__init__(config)

        self.auth = None
        self.username = self.config.get('username', None)
        self.password = self.config.get('password', None)
        self.hostname = self.config.get('hostname', None)
        self.port = self.config.get('port', 8080)
        self.url = "{}:{}/rest/items".format(self.hostname, self.port)

        if self.username and self.password:
            self.auth = base64.encodestring(
                '%s:%s' % (self.username, self.password)).replace('\n', '')

    def _headers(self):
        payload = {
            "Content-type": "text/plain",
            "Accept": "application/json"
        }
        if self.auth:
            payload['Authentication'] = "Basic {}".format(self.auth)
        return payload

    def _get(self, key):
        url = "{}/{}".format(self.url, key) if key else self.url
        payload = {'type': 'json'}
        req = requests.get(url, params=payload, headers=self._headers())
        return self._parse_req(req)

    def _put(self, key, value):
        url = "{}/{}/state".format(self.url, key)
        req = requests.put(url, data=value, headers=self._headers())
        return self._parse_req(req)

    def _post(self, key, value):
        url = "{}/{}".format(self.url, key)
        req = requests.post(url, data=value, headers=self._headers())
        return self._parse_req(req)

    def _parse_req(self, req):
        req.raise_for_status()
        try:
            return req.json()
        except:
            return req.text
