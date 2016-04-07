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


class VMAddNic(BaseAction):

    def run(self, vm_id, vm_name, network_name,
            nictype, stayconnected, wakeonlan):
        # create object itmes of key components
        checkinputs.one_of_two_strings(vm_id, vm_name, "ID or Name")

        vm = inventory.get_virtualmachine(self.si_content, vm_id, vm_name)
        network_obj = inventory.get_network(self.si_content, name=network_name)

        vm_reconfig_spec = self.get_vm_reconfig_spec(network_obj,
                                                     stayconnected,
                                                     nictype,
                                                     wakeonlan)

        add_vnic_task = vm.ReconfigVM_Task(spec=vm_reconfig_spec)
        successfully_added_vnic = self._wait_for_task(add_vnic_task)

        return {'state': successfully_added_vnic}

    def get_vm_reconfig_spec(self, network_obj,
                             stay_connected, network_type, wake_on_lan):
        network_spec = vim.vm.device.VirtualDeviceSpec()
        network_spec.operation = vim.vm.device.VirtualDeviceSpec.Operation.add

        if network_type.lower() == 'e1000':
            network_spec.device = vim.vm.device.VirtualE1000()
        elif network_type.lower() == 'flexible':
            network_spec.device = vim.vm.device.VirtualPCNet32()
        elif network_type.lower() == 'vmxnet':
            network_spec.device = vim.vm.device.VirtualVmxnet()
        elif network_type.lower() == 'enhancedvmxnet':
            network_spec.device = vim.vm.device.VirtualVmxnet2()
        elif network_type.lower() == 'vmxnet3':
            network_spec.device = vim.vm.device.VirtualVmxnet3()
        else:
            network_spec.device = vim.vm.device.VirtualEthernetCard()

        network_spec.device.wakeOnLanEnabled = wake_on_lan
        network_spec.device.deviceInfo = vim.Description()
        network_spec.device.backing = \
            vim.vm.device.VirtualEthernetCard.NetworkBackingInfo()
        network_spec.device.backing.network = network_obj
        network_spec.device.backing.deviceName = network_obj.name

        network_spec.device.connectable = \
            vim.vm.device.VirtualDevice.ConnectInfo()
        network_spec.device.connectable.startConnected = stay_connected
        network_spec.device.connectable.allowGuestControl = True

        # creating reconfig spec
        vm_reconfig_spec = vim.vm.ConfigSpec()
        vm_reconfig_spec.deviceChange = [network_spec]
        return vm_reconfig_spec
