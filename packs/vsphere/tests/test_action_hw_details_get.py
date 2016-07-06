import yaml
from mock import Mock, MagicMock

from vsphere_base_action_test_case import VsphereBaseActionTestCase

from vm_hw_details_get import GetVMDetails


__all__ = [
    'GetVMDetailsTestCase'
]


class GetVMDetailsTestCase(VsphereBaseActionTestCase):
    __test__ = True
    action_cls = GetVMDetails

    def test_run_blank_input(self):
        action = self.get_action_instance(self.new_config)

        self.assertRaises(ValueError, action.run, vm_ids=None, vm_names=None, vsphere="default")

