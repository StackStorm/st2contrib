"""Generated test for checking pynos based actions
"""
import xml.etree.ElementTree as ET
from st2tests.base import BaseActionTestCase
from interface_vrrp_vip import interface_vrrp_vip

__all__ = [
    'TestInterfaceVrrpVip'
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


class TestInterfaceVrrpVip(BaseActionTestCase):
    """Test holder class
    """
    action_cls = interface_vrrp_vip

    def test_action(self):
        """Generated test to check action
        """
        action = self.get_action_instance()
        mock_callback = MockCallback()
        kwargs = {
            'username': '',
            'rbridge_id': '224',
            'ip': '',
            'vrid': '10',
            'vip': '10.9.2.1',
            'int_type': 'gigabitethernet',
            'password': '',
            'port': '22',
            'name': '10/0/1',
            'test': True,
            'callback': mock_callback.callback
        }

        action.run(**kwargs)

        expected_xml = (
            '<config><interface xmlns="urn:brocade.com:mgmt:brocade-interface"'
            '><gigabitethernet><name>10/0/1</name><vrrp xmlns="urn:brocade.com'
            ':mgmt:brocade-vrrp"><vrid>10</vrid><version>3</version><virtual-i'
            'p><virtual-ipaddr>10.9.2.1</virtual-ipaddr></virtual-ip></vrrp></'
            'gigabitethernet></interface></config>'
        )

        self.assertTrue(expected_xml, mock_callback.returned_data)
