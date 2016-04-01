from pyVmomi import vim

from vmwarelib.actions import BaseAction


class SetVM(BaseAction):
    def run(self, vm, alternate_guest_name=None, description=None, guest_id=None, memory_mb=None,
            name=None, num_cpu=None, vm_swapfile_policy=None):
        vm_swapfile_policy = vm_swapfile_policy.lower() if vm_swapfile_policy else None

        si = self.si

        vm_obj = vim.VirtualMachine(vm, stub=si._stub)

        # convert ids to stubs
        spec = vim.vm.ConfigSpec()
        spec.alternateGuestName = alternate_guest_name
        spec.annotation = description
        spec.guestId = guest_id
        spec.memoryMB = memory_mb
        spec.name = name
        spec.numCPUs = num_cpu
        if vm_swapfile_policy == 'inhostdatastore':
            spec.swapPlacement = 'hostLocal'
        elif vm_swapfile_policy == 'withvm':
            spec.swapPlacement = 'vmDirectory'

        task = vm_obj.ReconfigVM_Task(spec)

        success = self._wait_for_task(task)

        return {'success': success}
