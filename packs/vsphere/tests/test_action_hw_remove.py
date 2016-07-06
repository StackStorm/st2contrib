import yaml
from mock import Mock, MagicMock

from vsphere_base_action_test_case import VsphereBaseActionTestCase

from vm_hw_remove import VMRemove


__all__ = [
    'GetVMDetailsTestCase'
]


class VMRemoveTestCase(VsphereBaseActionTestCase):
    __test__ = True
    action_cls = VMRemove

    #def test_run_blank_input(self):
        #action = self.get_action_instance(self.new_config)
        #self.assertRaises(ValueError, action.run, vm_names=None, vsphere="default")

