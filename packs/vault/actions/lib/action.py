from st2actions.runners.pythonrunner import Action

import hvac

class VaultBaseAction(Action):

    def __init__(self, config):
        super(VaultBaseAction, self).__init__(config)
        self.vault = self._get_client()

    def _get_client(self):
        url = self.config['url']
        token = self.config['token']
        cert = self.config['cert']
        verify = self.config['verify']

        client = hvac.Client(url=url, token=token, cert=cert, verify=verify)
        return client
