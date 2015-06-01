from st2actions.runners.pythonrunner import Action


class TravisCI(Action):
    def __init__(self, config):
        super(TravisCI, self).__init__(config)
        self.travis = self._init_conn()

    def _init_conn(self):
        travis = {'User_Agent': self.config['User-Agent'],
                  'Accept': self.config['Accept'],
                  'Host': self.config['Host'], }
        return travis
