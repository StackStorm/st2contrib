from lib import action


class DigitalOceanManager(action.BaseAction):

    def run(self, **kwargs):
      action = kwargs['action']
      del kwargs['action']
      cls = kwargs['cls']
      del kwargs['cls']
      return self.do_action(cls, action, **kwargs)
