from pyVmomi import vim

from vmwarelib import inventory
from vmwarelib.actions import BaseAction


class StopVM(BaseAction):

    def run(self, vm, kill=False):
        # convert ids to stubs
        vm_obj = inventory.get_virtualmachine(self.si_content, moid=vm_id)
        if kill:
            vm_obj.TerminateVM()
            success = true
        else:
            task = vm_obj.PowerOffVM_Task()
            success = self._wait_for_task(task)
        return {'success': success}
