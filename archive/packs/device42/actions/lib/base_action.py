import requests
from st2actions.runners.pythonrunner import Action


class BaseAction(Action):
    def __init__(self, config):
        super(BaseAction, self).__init__(config)

        self.d42_server = self.config.get('d42_server', None)
        if not self.d42_server:
            raise ValueError('"d42_server" config value is required')

        self.d42_username = self.config.get('d42_username', None)
        if not self.d42_username:
            raise ValueError('"d42_username" config value is required')

        self.d42_password = self.config.get('d42_password', None)
        if not self.d42_password:
            raise ValueError('"d42_password" config value is required')

        self.verify = self.config.get('verify_certificate', False)

    def getAPI(self, endpoint, params):
        r = requests.get("%s%s" % (self.d42_server, endpoint),
                         params=params,
                         auth=(self.d42_username, self.d42_password),
                         verify=self.verify
                         )

        return r.json()
