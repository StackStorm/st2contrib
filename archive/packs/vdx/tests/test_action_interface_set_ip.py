"""Generated test for checking pynos based actions
"""
import xml.etree.ElementTree as ET
from st2tests.base import BaseActionTestCase
from interface_set_ip import interface_set_ip

__all__ = [
    'TestInterfaceSetIp'
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


class TestInterfaceSetIp(BaseActionTestCase):
    """Test holder class
    """
    action_cls = interface_set_ip

    def test_action(self):
        """Generated test to check action
        """
        action = self.get_action_instance()
        mock_callback = MockCallback()
        kwargs = {
            'username': '',
            'password': '',
            'ip_addr': '10.10.0.1/24',
            'inter_type': 'tengigabitethernet',
            'ip': '',
            'inter': '10/0/1',
            'port': '22',
            'test': True,
            'callback': mock_callback.callback
        }

        action.run(**kwargs)

        expected_xml = (
            '<config><interface xmlns="urn:brocade.com:mgmt:brocade-interface"'
            '><tengigabitethernet><name>10/0/1</name><ip><ip-config xmlns="urn'
            ':brocade.com:mgmt:brocade-ip-config"><address><address>10.10.0.1/'
            '24</address></address></ip-config></ip></tengigabitethernet></int'
            'erface></config>'
        )

        self.assertTrue(expected_xml, mock_callback.returned_data)
