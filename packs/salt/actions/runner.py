import copy
import json
import requests

from st2actions.runners.pythonrunner import Action


class SaltPacket(object):
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


class SaltRunnerAction(Action):

    def __init__(self, config):
        super(SaltRunnerAction, self).__init__(config=config)
        self.url = self.config.get('api_url', None)
        self.username = self.config.get('username', None)
        self.password = self.config.get('password', None)
        self.data = SaltPacket('runner').data
        self.data['username'] = self.username
        self.data['password'] = self.password

    def run(self, cmd, args=None, **kwargs):
        '''
        CLI Examples:

            st2 run salt.runner manage.down
            st2 run salt.runner manage.down removekeys=True
        '''
        self.data['fun'] = cmd
        if args:
            self.data['arg'] = [args]
        if kwargs:
            self.data['kwargs'] = kwargs
        resp = requests.post("{0}/run".format(self.url),
                             headers={'content-type': 'application/json',
                                      'charset': 'utf-8'},
                             data=json.dumps(self.data),
                             verify=True)
        return resp.json()
