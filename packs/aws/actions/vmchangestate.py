from lib import action


class ChangeVMState(action.BaseAction):

    def run(self, state, instance_id):
        return self.ec2.changeVmState(state, instance_id)
