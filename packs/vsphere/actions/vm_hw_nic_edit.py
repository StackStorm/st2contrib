from pyVmomi import vim

from vmwarelib import inventory
from vmwarelib import checkinputs
from vmwarelib.actions import BaseAction


class VMNicEdit(BaseAction):

    def run(self, vm_id, vm_name, network_adapter, network_name):
        # check means of finding the VM was provided
        checkinputs.vm_identifier(vm_id, vm_name)
        # convert ids to stubs
        vm = inventory.get_virtualmachine(self.si_content,
                                          moid=vm_id,
                                          name=vm_name)
        network_obj = inventory.get_network(self.si_content,
                                            name=network_name)

        # find correct NIC
        for device in vm.config.hardware.device:
            if isinstance(device, vim.vm.device.VirtualEthernetCard)\
                    and device.deviceInfo.label == network_adapter:
                nic = device

        #Different test method due to fact that object
        #isn't instantiated if not found
        try:
            nic
        except:
            raise Exception('Unable to find Network Adapter provided')

        # Create object for new Specification
        new_spec = vim.vm.device.VirtualDeviceSpec()
        new_spec.operation = vim.vm.device.VirtualDeviceSpec.Operation.edit
        new_spec.device = nic

        #If network name provided assign new network
        # Room to expand the following to set additional flags/values
        if network_name:
            new_spec.device.backing.network = network_obj
            new_spec.device.backing.deviceName = network_obj.name
            new_spec.device.deviceInfo.summary = network_obj.name

        #format changes for config spec update
        dev_changes = []
        dev_changes.append(new_spec)
        spec = vim.vm.ConfigSpec()
        spec.deviceChange = dev_changes

        task = vm.ReconfigVM_Task(spec)
        self._wait_for_task(task)

        return {'state': str(task.info.state)}
