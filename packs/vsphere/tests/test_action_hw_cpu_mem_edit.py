import yaml
from mock import Mock, MagicMock

from vsphere_base_action_test_case import VsphereBaseActionTestCase

from vm_hw_cpu_mem_edit import VMCPUMemEdit


__all__ = [
    'GetVMDetailsTestCase'
]


class VMCPUMemEditTestCase(VsphereBaseActionTestCase):
    __test__ = True
    action_cls = VMCPUMemEdit

    def test_run_blank_identifier_input(self):
        action = self.get_action_instance(self.new_config)
        self.assertRaises(ValueError, action.run, vm_id=None, vm_name=None, cpu_edit=1, mem_edit=1,  vsphere="default")


