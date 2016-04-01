from pyVmomi import vim

from vmwarelib import inventory
from vmwarelib import checkinputs
from vmwarelib.actions import BaseAction


class VMCPUMemFlex(BaseAction):

    def run(self, vm_id, vm_name, cpu_flex, mem_flex):
        # check a means of finding the VM has been provided
        checkinputs.vm_identifier(vm_id, vm_name)

        vm = inventory.get_virtualmachine(self.si_content,
                                          moid=vm_id,
                                          name=vm_name)
        spec = vim.vm.ConfigSpec()
        if cpu_flex:
            spec.numCPUs = cpu_flex
        if mem_flex:
            spec.memoryMB = mem_flex * 1024

        task = vm.ReconfigVM_Task(spec)
        self._wait_for_task(task)

        return {'state': str(task.info.state)}
