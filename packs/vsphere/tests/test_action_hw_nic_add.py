import yaml
from mock import Mock, MagicMock

from vsphere_base_action_test_case import VsphereBaseActionTestCase

from vm_hw_nic_add import VMAddNic


__all__ = [
    'GetVMDetailsTestCase'
]


class VMAddNicTestCase(VsphereBaseActionTestCase):
    __test__ = True
    action_cls = VMAddNic

    def test_run_blank_identifier_input(self):
        action = self.get_action_instance(self.new_config)
        self.assertRaises(ValueError, action.run, vm_id=None,
                          vm_name=None, network_name=None,
                          nictype=None, stayconnected=None,
                          wakeonlan=None,  vsphere="default")

