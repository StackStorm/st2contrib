from st2actions.runners.pythonrunner import Action
from lib.client import Client


class Icinga2Action(Action):

    def __init__(self, config):
        super(Icinga2Action, self).__init__(config)
        self.body = ''
        self.error = 0
        self.api_url = config['api_url']
        self.api_user = config['api_user']
        self.api_password = config['api_password']
        self.method = 'get'
        self.path = ''

    def run(self):
        pass

    def get_client(self):
        client = Client(self, self.api_url + self.path, self.api_user,
                        self.api_password, self.method)
        return client

    def get_error(self):
        return self.error

    def get_body(self):
        return self.body

    def set_body(self, body):
        self.body = body

    def set_method(self, method):
        self.method = method

    def get_method(self):
        return self.method

    def set_path(self, path):
        self.path = path

    def get_path(self):
        return self.path
