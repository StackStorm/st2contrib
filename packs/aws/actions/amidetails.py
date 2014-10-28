from lib import action


class AMIDetails(action.BaseAction):

    def run(self, ami_id):
        return self.ec2.getAMI(ami_id, "self")
