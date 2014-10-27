from lib import ec2, action


class CreateVM(action.BaseAction):

    def run(self, ami, instance_type):
        e = ec2.EC2(self.region)
        e.setup(True)
        return e.createVM(ami, instance_type)
