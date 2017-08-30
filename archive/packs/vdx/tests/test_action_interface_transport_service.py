"""Generated test for checking pynos based actions
"""
import xml.etree.ElementTree as ET
from st2tests.base import BaseActionTestCase
from interface_transport_service import interface_transport_service

__all__ = [
    'TestInterfaceTransportService'
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


class TestInterfaceTransportService(BaseActionTestCase):
    """Test holder class
    """
    action_cls = interface_transport_service

    def test_action(self):
        """Generated test to check action
        """
        action = self.get_action_instance()
        mock_callback = MockCallback()
        kwargs = {
            'username': '',
            'password': '',
            'service_id': '24',
            'ip': '',
            'vlan': '24',
            'port': '22',
            'test': True,
            'callback': mock_callback.callback
        }

        action.run(**kwargs)

        expected_xml = (
            '<config><interface-vlan xmlns="urn:brocade.com:mgmt:brocade-inter'
            'face"><interface><vlan><name>24</name><transport-service>24</tran'
            'sport-service></vlan></interface></interface-vlan></config>'
        )

        self.assertTrue(expected_xml, mock_callback.returned_data)
