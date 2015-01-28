from st2actions.runners.pythonrunner import Action
import pyrax

__all__ = [
    'PyraxBaseAction'
]

class PyraxBaseAction(Action):
    def __init__(self, config):
        super(PyraxBaseAction, self).__init__(config)
        self.pyrax = self._get_client()

    def _get_client(self):
        username = self.config['username']
        api_key = self.config['api_key']

        # Needs to be extracted to per-action
        region = self.config['region']

        pyrax.set_setting('identity_type', 'rackspace')
        pyrax.set_default_region(region)
        pyrax.set_credentials(username, api_key)

        return pyrax
