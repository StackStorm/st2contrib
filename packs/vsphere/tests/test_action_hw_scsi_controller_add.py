import yaml
from mock import Mock, MagicMock

from vsphere_base_action_test_case import VsphereBaseActionTestCase

from vm_hw_scsi_controller_add import VMAddSCSIController


__all__ = [
    'GetVMDetailsTestCase'
]


class VMAddSCSIControllerTestCase(VsphereBaseActionTestCase):
    __test__ = True
    action_cls = VMAddSCSIController

    def test_run_blank_identifier_input(self):
        action = self.get_action_instance(self.new_config)
        self.assertRaises(ValueError, action.run, vm_id=None,
                          vm_name=None, controller_type=None,
                          scsi_sharing=None, vsphere="default")

