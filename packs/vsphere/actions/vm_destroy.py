from vmwarelib import inventory
from vmwarelib.actions import BaseAction


class VMDestroy(BaseAction):

    def run(self, vm_id):
        # convert ids to stubs
        vm = inventory.get_virtualmachine(self.si_content, moid=vm_id)

        task = vm.Destroy_Task()
        success = self._wait_for_task(task)

        # verify status is running.
        return {"status": success}
