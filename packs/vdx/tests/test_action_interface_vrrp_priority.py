"""Generated test for checking pynos based actions
"""
import xml.etree.ElementTree as ET
from st2tests.base import BaseActionTestCase
from interface_vrrp_priority import interface_vrrp_priority

__all__ = [
    'TestInterfaceVrrpPriority'
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


class TestInterfaceVrrpPriority(BaseActionTestCase):
    """Test holder class
    """
    action_cls = interface_vrrp_priority

    def test_action(self):
        """Generated test to check action
        """
        action = self.get_action_instance()
        mock_callback = MockCallback()
        kwargs = {
            'username': '',
            'name': '10/0/2',
            'ip': '',
            'vrid': '10',
            'priority': '200',
            'int_type': 'tengigabitethernet',
            'ip_version': '4',
            'password': '',
            'port': '22',
            'test': True,
            'callback': mock_callback.callback
        }

        action.run(**kwargs)

        expected_xml = (
            '<config><interface xmlns="urn:brocade.com:mgmt:brocade-interface"'
            '><tengigabitethernet><name>10/0/2</name><vrrp xmlns="urn:brocade.'
            'com:mgmt:brocade-vrrp"><vrid>10</vrid><version>3</version><priori'
            'ty>200</priority></vrrp></tengigabitethernet></interface></config'
            '>'
        )

        self.assertTrue(expected_xml, mock_callback.returned_data)
