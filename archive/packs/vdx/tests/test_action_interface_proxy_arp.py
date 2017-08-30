"""Generated test for checking pynos based actions
"""
import xml.etree.ElementTree as ET
from st2tests.base import BaseActionTestCase
from interface_proxy_arp import interface_proxy_arp

__all__ = [
    'TestInterfaceProxyArp'
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


class TestInterfaceProxyArp(BaseActionTestCase):
    """Test holder class
    """
    action_cls = interface_proxy_arp

    def test_action(self):
        """Generated test to check action
        """
        action = self.get_action_instance()
        mock_callback = MockCallback()
        kwargs = {
            'username': '',
            'name': '10/0/2',
            'ip': '',
            'enabled': True,
            'int_type': 'tengigabitethernet',
            'password': '',
            'port': '22',
            'rbridge_id': '224',
            'test': True,
            'callback': mock_callback.callback
        }

        action.run(**kwargs)

        expected_xml = (
            '<config><interface xmlns="urn:brocade.com:mgmt:brocade-interface"'
            '><tengigabitethernet><name>10/0/2</name><ip><ip-config xmlns="urn'
            ':brocade.com:mgmt:brocade-ip-config"><proxy-arp /></ip-config></i'
            'p></tengigabitethernet></interface></config>'
        )

        self.assertTrue(expected_xml, mock_callback.returned_data)
