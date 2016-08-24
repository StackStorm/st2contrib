"""Generated test for checking pynos based actions
"""
import xml.etree.ElementTree as ET
from st2tests.base import BaseActionTestCase
from interface_private_vlan_type import interface_private_vlan_type

__all__ = [
    'TestInterfacePrivateVlanType'
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


class TestInterfacePrivateVlanType(BaseActionTestCase):
    """Test holder class
    """
    action_cls = interface_private_vlan_type

    def test_action(self):
        """Generated test to check action
        """
        action = self.get_action_instance()
        mock_callback = MockCallback()
        kwargs = {
            'username': '',
            'name': '10',
            'pvlan_type': 'primary',
            'ip': '',
            'password': '',
            'port': '22',
            'test': True,
            'callback': mock_callback.callback
        }

        action.run(**kwargs)

        expected_xml = (
            '<config><interface-vlan xmlns="urn:brocade.com:mgmt:brocade-inter'
            'face"><interface><vlan><name>10</name><private-vlan><pvlan-type-l'
            'eaf>primary</pvlan-type-leaf></private-vlan></vlan></interface></'
            'interface-vlan></config>'
        )

        self.assertTrue(expected_xml, mock_callback.returned_data)
