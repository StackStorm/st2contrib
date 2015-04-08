from functools import partial

from st2actions.runners.pythonrunner import Action
from requests import Request


class SaltPackage(object):
    _data = {"eauth": "pam",
             "username": "",
             "password": "",
             "client": "",
             "fun": ""}

    def __init__(self, client='local'):
        self._data['client'] = client

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, key_value=[]):
        key, value = key_value
        self._data[key] = value


class SaltAction(Action):

    def __init__(self, config):
        super(SaltAction, self).__init__(config=config)
        self.url = self.config.get('api_url', None)
        self.username = self.config.get('username', None)
        self.password = self.config.get('password', None)

    def generate_package(self, client='local'):
        self.data = SaltPackage(client).data
        self.data['username'] = self.username
        self.data['password'] = self.password

    def generate_request(self):
        req = Request('POST',
                      "{0}/run".format(self.url),
                      headers={'content-type': 'application/json',
                               'charset': 'utf-8'})
        return req.prepare()
