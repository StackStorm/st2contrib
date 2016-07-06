import yaml
from mock import Mock, MagicMock

from vsphere_base_action_test_case import VsphereBaseActionTestCase

from vm_hw_uuid_get import GetVMUUID


__all__ = [
    'GetVMDetailsTestCase'
]


class GetVMUUIDTestCase(VsphereBaseActionTestCase):
    __test__ = True
    action_cls = GetVMUUID

    def test_run_blank_identifier_input(self):
        action = self.get_action_instance(self.new_config)
        self.assertRaises(ValueError, action.run, vm_ids=None,
                          vm_names=None, vsphere="default")

