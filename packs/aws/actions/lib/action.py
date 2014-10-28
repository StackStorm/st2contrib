from lib import ec2
from st2actions.runners.pythonrunner import Action


class BaseAction(Action):

    def __init__(self, config):
        super(BaseAction, self).__init__(config)
        self.ec2 = ec2.EC2(config)
