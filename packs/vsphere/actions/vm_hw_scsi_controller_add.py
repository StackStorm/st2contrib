from pyVmomi import vim

from vmwarelib import inventory
from vmwarelib import checkinputs
from vmwarelib.actions import BaseAction


class VMAddSCSIController(BaseAction):

    def run(self, vm_id, vm_name, controller_type, scsi_sharing):
        # VM name or ID given?
        checkinputs.vm_identifier(vm_id, vm_name)

        # Create object for VM
        vm = inventory.get_virtualmachine(self.si_content, vm_id, vm_name)

        # Create SCSI Controller Object
        configspec = vim.vm.ConfigSpec()
        scsictrl = vim.vm.device.VirtualDeviceSpec()
        scsictrl.operation = vim.vm.device.VirtualDeviceSpec.Operation.add

        # Select object type
        if controller_type == 'ParaVirtual':
            scsictrl.device = vim.vm.device.ParaVirtualSCSIController()
        elif controller_type == 'BusLogic':
            scsictrl.device = vim.vm.device.VirtualBusLogicController()
        elif controller_type == 'LSILogic':
            scsictrl.device = vim.vm.device.VirtualLsiLogicController()
        elif controller_type == 'LSILogicSAS':
            scsictrl.device = vim.vm.device.VirtualLsiLogicSASController()

        # Set SCSI Bus Sharing type
        if scsi_sharing == 'None':
            scsictrl.device.sharedBus = 'noSharing'
        elif scsi_sharing == 'Physical':
                        scsictrl.device.sharedBus = 'physicalSharing'
        elif scsi_sharing == 'Virtual':
                        scsictrl.device.sharedBus = 'virtualSharing'

        # Create Task to add to VM
        configspec.deviceChange = [scsictrl]
        add_ctrl_task = vm.ReconfigVM_Task(configspec)
        successfully_added_ctrl = self._wait_for_task(add_ctrl_task)

        return {'state': successfully_added_ctrl}
