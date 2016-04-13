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
from vmwarelib.actions import BaseAction


class VMDiskAdd(BaseAction):

    def run(self, vm_id, disk_size, disk_type):
        vm = inventory.get_virtualmachine(self.si_content, vm_id)
        spec = vim.vm.ConfigSpec()

        # disk spec
        disk_spec = vim.vm.device.VirtualDeviceSpec()
        disk_spec.fileOperation = "create"
        disk_spec.operation = vim.vm.device.VirtualDeviceSpec.Operation.add
        disk_spec.device = vim.vm.device.VirtualDisk()
        disk_spec.device.backing = vim.vm.device.VirtualDisk.FlatVer2BackingInfo()
        if disk_type == 'thin':
            disk_spec.device.backing.thinProvisioned = True
        disk_spec.device.backing.diskMode = 'persistent'
        disk_spec.device.unitNumber = self.get_next_unit_number(vm)
        disk_spec.device.capacityInKB = disk_size * 1024 * 1024
        disk_spec.device.controllerKey = 1000

        spec.deviceChange = [disk_spec]

        # add disk and wait for task to complete
        add_disk_task = vm.ReconfigVM_Task(spec)
        successfully_added_disk = self._wait_for_task(add_disk_task)
        return {'state': successfully_added_disk}

    def get_next_unit_number(self, vm):
        # See https://github.com/whereismyjetpack/pyvmomi-community-samples/blob/
        # add-disk/samples/add_disk_to_vm.py
        unit_number = 0
        for dev in vm.config.hardware.device:
            if hasattr(dev.backing, 'fileName'):
                unit_number = int(dev.unitNumber) + 1
                # unit_number 7 reserved for scsi controller
                if unit_number == 7:
                    unit_number += 1
        return unit_number
