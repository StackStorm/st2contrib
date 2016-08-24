"""Generated test for checking pynos based actions
"""
import xml.etree.ElementTree as ET
from st2tests.base import BaseActionTestCase
from interface_add_vlan_int import interface_add_vlan_int

__all__ = [
    'TestInterfaceAddVlanInt'
]


class MockCallback(object):  # pylint:disable=too-few-public-methods
    """Class to hold mock callback and result
    """
    returned_data = None

    def callback(self, call, **kwargs):  # pylint:disable=unused-argument
        """Mock callback method
        """
        xml_result = ET.tostring(call)
        self.returned_data = xml_result


class TestInterfaceAddVlanInt(BaseActionTestCase):
    """Test holder class
    """
    action_cls = interface_add_vlan_int

    def test_action(self):
        """Generated test to check action
        """
        action = self.get_action_instance()
        mock_callback = MockCallback()
        kwargs = {
            'username': '',
            'ip': '',
            'password': '',
            'port': '22',
            'vlan_id': '44',
            'test': True,
            'callback': mock_callback.callback
        }

        action.run(**kwargs)

        expected_xml = (
            '<config><interface-vlan xmlns="urn:brocade.com:mgmt:brocade-inter'
            'face"><interface><vlan><name>44</name></vlan></interface></interf'
            'ace-vlan></config>'
        )

        self.assertTrue(expected_xml, mock_callback.returned_data)
