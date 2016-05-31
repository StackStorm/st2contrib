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


class NewNetworkAdapter(BaseAction):

    @staticmethod
    def get_vm_reconfig_spec(distributed_switch_obj, mac_address, network_obj, port_key,
                             stay_connected, network_type, wake_on_lan):
        # creating virtual device
        if network_type == 'e1000':
            virtual_network = vim.vm.device.VirtualE1000()
        elif network_type == 'flexible':
            virtual_network = vim.vm.device.VirtualPCNet32()
            lance_option = vim.vm.device.VirtualPCNet32Option()
            lance_option.supportsMorphing = True
        # TODO and question for Manas: We need to plug in that lance_option on something.
        # I could not find any class that uses VirtualPCNet32Option or any of its upstream classes.
        elif network_type == 'vmxnet':
            virtual_network = vim.vm.device.VirtualVmxnet()
        elif network_type == 'enhancedvmxnet':
            virtual_network = vim.vm.device.VirtualVmxnet2()
        elif network_type == 'vmxnet3':
            virtual_network = vim.vm.device.VirtualVmxnet3()
        else:
            virtual_network = vim.vm.device.VirtualEthernetCard()

        virtual_network.wakeOnLanEnabled = wake_on_lan
        connect_info = vim.vm.device.VirtualDevice.ConnectInfo()
        connect_info.startConnected = stay_connected
        virtual_network.connectable = connect_info
        if mac_address:
            virtual_network.macAddress = mac_address
            virtual_network.addressType = vim.vm.device.VirtualEthernetCardOption.MacTypes.manual

        # creating backing info
        backing_info = None
        if distributed_switch_obj:
            dvs_port_connection = vim.dvs.PortConnection()
            dvs_port_connection.switchUuid = distributed_switch_obj.uuid
            if port_key:
                dvs_port_connection.portKey = port_key
                port_criteria = vim.dvs.PortCriteria()
                port_criteria.portKey = port_key
                ports = distributed_switch_obj.FetchDVPorts(port_criteria)
                dvs_port_connection.portgroupKey = ports[0].portgroupKey
            backing_info = vim.vm.device.VirtualEthernetCard.DistributedVirtualPortBackingInfo()
            backing_info.port = dvs_port_connection

        if network_obj:
            backing_info = vim.vm.device.VirtualEthernetCard.NetworkBackingInfo()
            backing_info.network = network_obj
            backing_info.deviceName = network_obj.name

        virtual_network.backing = backing_info

        # creating network device spec
        network_spec = vim.vm.device.VirtualDeviceSpec()
        network_spec.device = virtual_network
        network_spec.operation = vim.vm.device.VirtualDeviceSpec.Operation.add

        # creating reconfig spec
        vm_reconfig_spec = vim.vm.ConfigSpec()
        vm_reconfig_spec.deviceChange = [network_spec]
        return vm_reconfig_spec

    def run(self, vms, distributed_switch=None, mac_address=None, network_name=None, port_key=None,
            stay_connected=False, network_type='Flexible', wake_on_lan=False):
        network_type = network_type.lower() if network_type else None
        si = self.si
        si_content = si.RetrieveContent()

        vm_objs = [vim.VirtualMachine(moid, stub=si._stub) for moid in vms]
        # by checking the name property, the vms' existance is checked.
        [vm_obj.name for vm_obj in vm_objs]

        distributed_switch_obj = None
        if distributed_switch:
            distributed_switch_obj = vim.DistributedVirtualSwitch(distributed_switch, stub=si._stub)
            # by checking the name property, the distributed switch existence is checked.
            distributed_switch_obj.name

        network_obj = None
        if network_name:
            network_obj = inventory.get_network(si_content, name=network_name)
            # by checking the name property, the network existence is checked.
            network_obj.name

        result = []
        for vm in vm_objs:
            vm_reconfig_spec = NewNetworkAdapter.get_vm_reconfig_spec(distributed_switch_obj,
                mac_address, network_obj, port_key, stay_connected, network_type, wake_on_lan)
            add_disk_task = vm.ReconfigVM_Task(spec=vm_reconfig_spec)
            successfully_added_network = self._wait_for_task(add_disk_task)
            result.append({
                "vm_moid": vm._GetMoId(),
                "success": successfully_added_network
            })

        return result
