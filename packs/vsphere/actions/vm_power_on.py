import eventlet

from pyVmomi import vim

from vmwarelib import inventory
from vmwarelib.actions import BaseAction


class VMPowerOn(BaseAction):

    def run(self, vm_id):
        # convert ids to stubs
        vm = inventory.get_virtualmachine(self.si_content, moid=vm_id)
        task = vm.PowerOnVM_Task(None)
        while task.info.state == vim.TaskInfo.State.running:
            eventlet.sleep(1)
        return {'state': str(task.info.state)}
