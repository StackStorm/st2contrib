from st2actions.runners.pythonrunner import Action

from lib.puppet_client import PuppetHTTPAPIClient


class PuppetBasePythonAction(Action):
    def __init__(self, config):
        super(PuppetBasePythonAction, self).__init__(config=config)
        self.client = self._get_client()

    def _get_client(self):
        client = PuppetHTTPAPIClient(master_hostname=self.config['hostname'],
                                     master_port=self.config['port'],
                                     client_cert_path=self.config['client_cert_path'],
                                     client_cert_key_path=self.config['client_cert_key_path'],
                                     ca_cert_path=self.config['ca_cert_path'])

        return client
