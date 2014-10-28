from lib import action


class ChangeVMState(action.BaseAction):

    def run(self, instance_id, iponly):
        return self.ec2.getInstanceDetails(instance_id, iponly)
