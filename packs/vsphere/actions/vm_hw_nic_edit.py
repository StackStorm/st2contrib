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


class VMNicEdit(BaseAction):

    def run(self, vm_id, vm_name, network_adapter, network_name):
        # check means of finding the VM was provided
        checkinputs.one_of_two_strings(vm_id, vm_name, "ID or Name")
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

        # Different test method due to fact that object
        # isn't instantiated if not found
        try:
            nic
        except:
            raise Exception('Unable to find Network Adapter provided')

        # Create object for new Specification
        new_spec = vim.vm.device.VirtualDeviceSpec()
        new_spec.operation = vim.vm.device.VirtualDeviceSpec.Operation.edit
        new_spec.device = nic

        # If network name provided assign new network
        # Room to expand the following to set additional flags/values
        if network_name:
            new_spec.device.backing.network = network_obj
            new_spec.device.backing.deviceName = network_obj.name
            new_spec.device.deviceInfo.summary = network_obj.name

        # format changes for config spec update
        dev_changes = []
        dev_changes.append(new_spec)
        spec = vim.vm.ConfigSpec()
        spec.deviceChange = dev_changes

        task = vm.ReconfigVM_Task(spec)
        self._wait_for_task(task)

        return {'state': str(task.info.state)}
