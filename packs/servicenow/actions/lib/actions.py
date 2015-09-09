from st2actions.runners.pythonrunner import Action
import servicenow_rest.api as sn


class BaseAction(Action):
    def __init__(self, config):
        super(BaseAction, self).__init__(config)
        self.client = self._get_client()

    def _get_client(self):
        instance_name = self.config['instance_name']
        username = self.config['username']
        password = self.config['password']

        return sn.Client(instance_name, username, password)
