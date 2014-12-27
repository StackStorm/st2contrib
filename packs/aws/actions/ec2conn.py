from lib import action


class EC2Conn(action.BaseAction):

    def run(self, **kwargs):
      action = kwargs['action']
      del kwargs['action']
      return self.ec2_action(action, **kwargs)
