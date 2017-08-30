# Licensed to the StackStorm, Inc ('StackStorm') under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from pyVmomi import vim

from vmwarelib import inventory
from vmwarelib import checkinputs
from vmwarelib.actions import BaseAction


class VMAddSCSIController(BaseAction):

    def run(self, vm_id, vm_name, controller_type, scsi_sharing, vsphere=None):
        """
        Add SCSI controller to Virtual Machine

        Args:
        - vm_id: Moid of Virtual Machine to edit
        - vm_name: Name of Virtual Machine to edit
        - controller_type: Type of Controller to add
        - scsi_sharing: type of sharing for scsi adapter
        - vsphere: Pre-configured vsphere connection details (config.yaml)

        Returns:
        - dict: state true/false
        """

        # VM name or ID given?
        checkinputs.one_of_two_strings(vm_id, vm_name, "ID or Name")

        self.establish_connection(vsphere)

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
