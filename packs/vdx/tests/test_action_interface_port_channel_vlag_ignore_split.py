"""Generated test for checking pynos based actions
"""
import xml.etree.ElementTree as ET
from st2tests.base import BaseActionTestCase
from interface_port_channel_vlag_ignore_split import interface_port_channel_vlag_ignore_split

__all__ = [
    'TestInterfacePortChannelVlagIgnoreSplit'
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


class TestInterfacePortChannelVlagIgnoreSplit(BaseActionTestCase):
    """Test holder class
    """
    action_cls = interface_port_channel_vlag_ignore_split

    def test_action(self):
        """Generated test to check action
        """
        action = self.get_action_instance()
        mock_callback = MockCallback()
        kwargs = {
            'username': '',
            'name': '1',
            'ip': '',
            'password': '',
            'enabled': True,
            'port': '22',
            'test': True,
            'callback': mock_callback.callback
        }

        action.run(**kwargs)

        expected_xml = (
            '<config><interface xmlns="urn:brocade.com:mgmt:brocade-interface"'
            '><port-channel><name>1</name><vlag><ignore-split /></vlag></port-'
            'channel></interface></config>'
        )

        self.assertTrue(expected_xml, mock_callback.returned_data)
