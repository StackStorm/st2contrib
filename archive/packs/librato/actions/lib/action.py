from st2actions.runners.pythonrunner import Action

# https://github.com/librato/python-librato
import librato


class LibratoBaseAction(Action):
    def __init__(self, config):
        super(LibratoBaseAction, self).__init__(config)
        self.librato = self._get_client()

    def _get_client(self):
        user = self.config['user']
        token = self.config['token']

        client = librato.connect(user, token)
        return client
