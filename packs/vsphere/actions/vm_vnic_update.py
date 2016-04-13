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


class VMUpdateNic(BaseAction):

    def run(self, vm_id, network_id, vnic_key, ip, subnet, gateway=None, domain=None):
        # convert ids to stubs
        virtualmachine = inventory.get_virtualmachine(self.si_content, vm_id)
        network = inventory.get_network(self.si_content, network_id)
        vnic = self._get_vnic_device(virtualmachine, vnic_key)

        # add new vnic
        configspec = vim.vm.ConfigSpec()
        nic = vim.vm.device.VirtualDeviceSpec()
        nic.operation = vim.vm.device.VirtualDeviceSpec.Operation.edit
        nic.device = vim.vm.device.VirtualVmxnet3()
        nic.device.wakeOnLanEnabled = True
        nic.device.addressType = 'assigned'
        nic.device.key = vnic.key
        nic.device.deviceInfo = vim.Description()
        nic.device.deviceInfo.label = 'Network Adapter-%s' % (ip)
        nic.device.deviceInfo.summary = 'summary'
        nic.device.backing = vim.vm.device.VirtualEthernetCard.DistributedVirtualPortBackingInfo()
        nic.device.backing.port = vim.dvs.PortConnection()
        nic.device.backing.port.switchUuid = network.config.distributedVirtualSwitch.uuid
        nic.device.backing.port.portgroupKey = network.config.key
        nic.device.connectable = vim.vm.device.VirtualDevice.ConnectInfo()
        nic.device.connectable.startConnected = True
        nic.device.connectable.allowGuestControl = True
        configspec.deviceChange = [nic]
        add_vnic_task = virtualmachine.ReconfigVM_Task(configspec)
        successfully_added_vnic = self._wait_for_task(add_vnic_task)

        if not successfully_added_vnic:
            return self._format_result(successfully_added_vnic, 'Failed to update nic.')

        adaptermap = vim.vm.customization.AdapterMapping()
        adaptermap.adapter = vim.vm.customization.IPSettings()
        adaptermap.adapter.ip = vim.vm.customization.FixedIp()
        adaptermap.adapter.ip.ipAddress = ip
        adaptermap.adapter.subnetMask = subnet
        adaptermap.adapter.gateway = gateway
        adaptermap.adapter.dnsDomain = domain

        globalip = vim.vm.customization.GlobalIPSettings()

        ident = vim.vm.customization.LinuxPrep()
        ident.domain = domain
        ident.hostName = vim.vm.customization.FixedName()
        ident.hostName.name = virtualmachine.name

        customspec = vim.vm.customization.Specification()
        customspec.identity = ident
        customspec.nicSettingMap = [adaptermap]
        customspec.globalIPSettings = globalip

        try:
            customize_task = virtualmachine.Customize(spec=customspec)
            successfully_customized = self._wait_for_task(customize_task)
        except:
            self.logger.exception('Failed to create customization spec.')
            raise
        msg = 'Updated nic and assigned IP.' if successfully_customized else 'Failed to assign ip.'
        return self._format_result(successfully_customized, msg=msg)

    @staticmethod
    def _get_vnic_device(vm, vnic_key=-1):
        verify_vnic = vnic_key != -1
        for device in vm.config.hardware.device:
            # If a key is passed in verify that it is a vnic else look for the first vnic.
            if verify_vnic and device.key == vnic_key:
                is_vnic = isinstance(device, vim.vm.device.VirtualEthernetCard)
                if not is_vnic:
                    raise Exception('Invalid device key %s' % str(vnic_key))
                return device
            elif not verify_vnic:
                is_vnic = isinstance(device, vim.vm.device.VirtualEthernetCard)
                if is_vnic:
                    return device
        # ending up here mean a bad key or no vnic.
        raise Exception('vnic for device %s not found' % str(vnic_key))

    @staticmethod
    def _format_result(state, msg=None):
        return {'state': state, 'msg': msg}
