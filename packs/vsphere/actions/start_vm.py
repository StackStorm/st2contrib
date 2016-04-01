from pyVmomi import vim

from vmwarelib.actions import BaseAction


class StartVM(BaseAction):

    def run(self, vm):
        si = self.si
        vm_obj = vim.VirtualMachine(vm, stub=si._stub)

        task = vm_obj.PowerOnVM_Task(None)
        success = self._wait_for_task(task)
        return {'success': success}
