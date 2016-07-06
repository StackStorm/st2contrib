import yaml
from mock import Mock, MagicMock

from vsphere_base_action_test_case import VsphereBaseActionTestCase

from vm_hw_barebones_create import VMCreateBareBones


__all__ = [
    'GetVMDetailsTestCase'
]


class VMCreateBareBonesTestCase(VsphereBaseActionTestCase):
    __test__ = True
    action_cls = VMCreateBareBones

    #def test_run_blank_input(self):
        #action = self.get_action_instance(self.new_config)
        #self.assertRaises(ValueError, action.run, vm_names=None, vsphere="default")

