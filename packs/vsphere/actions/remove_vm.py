from pyVmomi import vim

from vmwarelib import inventory
from vmwarelib.actions import BaseAction


class RemoveVM(BaseAction):

    def run(self, vm, delete_permanently):
        si = self.si

        vm_obj = vim.VirtualMachine(vm, stub=si._stub)
        if delete_permanently:
            task = vm_obj.Destroy_Task()
            success = self._wait_for_task(task)
        else:
            vm_obj.UnregisterVM()
            success = True

        return {"success": success}
