import uuid

from pyVmomi import vim

from vmwarelib import inventory
from vmwarelib.actions import BaseAction


class VMAddNic(BaseAction):

    def run(self, vm_id, network_id, ip, subnet, gateway=None, domain=None):
        # convert ids to stubs
        virtualmachine = inventory.get_virtualmachine(self.si_content, vm_id)
        network = inventory.get_network(self.si_content, network_id)

        # add new vnic
        configspec = vim.vm.ConfigSpec()
        nic = vim.vm.device.VirtualDeviceSpec()
        nic.operation = vim.vm.device.VirtualDeviceSpec.Operation.add  # or edit if a device exists
        nic.device = vim.vm.device.VirtualVmxnet3()
        nic.device.wakeOnLanEnabled = True
        nic.device.addressType = 'assigned'
        # docs recommend using unique negative integers as temporary keys.
        # See https://github.com/vmware/pyvmomi/blob/master/docs/vim/vm/device/VirtualDevice.rst
        nic.device.key = -1
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

        # customize VM
        cust_item = vim.CustomizationSpecItem()
        cust_specinfo = vim.CustomizationSpecInfo()
        cust_specinfo.name = 'assignip-' + str(uuid.uuid4())
        cust_specinfo.type = 'Linux'
        cust_item.info = cust_specinfo

        # fixed ip
        cust_spec = vim.vm.customization.Specification()
        cust_item.spec = cust_spec
        ip_adapter_mapping = vim.vm.customization.AdapterMapping()
        ip_adapter_mapping.adapter = vim.vm.customization.IPSettings()
        ip_adapter_mapping.adapter.ip = vim.vm.customization.FixedIp()
        ip_adapter_mapping.adapter.ip.ipAddress = ip
        ip_adapter_mapping.adapter.subnetMask = subnet
        ip_adapter_mapping.adapter.gateway = gateway
        ip_adapter_mapping.adapter.dnsDomain = domain
        cust_spec.nicSettingMap = [ip_adapter_mapping]
        cust_spec.identity = vim.vm.customization.LinuxPrep()
        cust_spec.identity.hostName = vim.vm.customization.PrefixNameGenerator()
        cust_spec.identity.hostName.base = 'st2'
        cust_spec.identity.domain = 'demo.net'
        cust_spec.globalIPSettings = vim.vm.customization.GlobalIPSettings()

        try:
            self.si_content.customizationSpecManager.CreateCustomizationSpec(cust_item)
        except:
            self.logger.exception('Failed to create customization spec.')
            raise

        return {'state': successfully_added_vnic}
