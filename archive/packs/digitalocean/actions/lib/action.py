import digitalocean
from st2actions.runners.pythonrunner import Action


class BaseAction(Action):

    def __init__(self, config):
        super(BaseAction, self).__init__(config)
        self._token = config['token']

    def do_action(self, cls, action, **kwargs):
        obj = getattr(digitalocean, cls)(token=self._token)
        return getattr(obj, action)(**kwargs)
