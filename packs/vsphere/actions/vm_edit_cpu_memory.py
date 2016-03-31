import eventlet

from pyVmomi import vim

from vmwarelib import inventory
from vmwarelib.actions import BaseAction


class VMEditCPUMem(BaseAction):

    def run(self, vm_id, cpu, memory):
        # convert ids to stubs
        vm = inventory.get_virtualmachine(self.si_content, moid=vm_id)
        spec = vim.vm.ConfigSpec()
        spec.numCPUs = cpu
        spec.memoryMB = memory
        task = vm.ReconfigVM_Task(spec)

        while task.info.state == vim.TaskInfo.State.running:
            eventlet.sleep(1)

        return {'state': str(task.info.state)}
