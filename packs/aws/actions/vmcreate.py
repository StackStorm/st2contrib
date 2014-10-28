from lib import action


class CreateVM(action.BaseAction):

    def run(self, ami, instance_type):
        self.ec2.setup(True)
        return self.ec2.createVM(ami, instance_type)
