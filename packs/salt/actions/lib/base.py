from st2actions.runners.pythonrunner import Action
from requests import Request
import logging
from utils import sanitize_payload

logger = logging.getLogger(__name__)


class SaltPackage(object):
    _expression_forms = [
        'glob',
        'grain',
        'pillar',
        'nodegroup',
        'list',
        'compound'
    ]
    _data = {"eauth": "",
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
        self.eauth = self.config.get('eauth', None)
        self.username = self.config.get('username', None)
        self.password = self.config.get('password', None)

    def generate_package(self, client='local', cmd=None, **kwargs):
        self.data = SaltPackage(client).data
        self.data['eauth'] = self.eauth
        self.data['username'] = self.username
        self.data['password'] = self.password
        if cmd:
            self.data['fun'] = cmd
        if client is 'local':
            self.data['tgt'] = kwargs.get('target', '*')
            self.data['expr_form'] = kwargs.get('expr_form', 'glob')
        if kwargs['data'] is not None:
            d = dict()
            d['kwarg'] = kwargs['data']['kwargs']
            self.data.update(d)
        logging.info("Sending To Salt API: {0}".format(sanitize_payload(('username', 'password'), self.data)))

    def generate_request(self):
        req = Request('POST',
                      "{0}/run".format(self.url),
                      headers={'content-type': 'application/json',
                               'charset': 'utf-8'})
        return req.prepare()
