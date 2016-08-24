"""Generated test for checking pynos based actions
"""
import xml.etree.ElementTree as ET
from st2tests.base import BaseActionTestCase
from interface_channel_group import interface_channel_group

__all__ = [
    'TestInterfaceChannelGroup'
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


class TestInterfaceChannelGroup(BaseActionTestCase):
    """Test holder class
    """
    action_cls = interface_channel_group

    def test_action(self):
        """Generated test to check action
        """
        action = self.get_action_instance()
        mock_callback = MockCallback()
        kwargs = {
            'username': '',
            'name': '10/0/1',
            'ip': '',
            'port_int': '4',
            'channel_type': 'standard',
            'mode': 'active',
            'int_type': 'tengigabitethernet',
            'password': '',
            'port': '22',
            'delete': False,
            'test': True,
            'callback': mock_callback.callback
        }

        action.run(**kwargs)

        expected_xml = (
            '<config><interface xmlns="urn:brocade.com:mgmt:brocade-interface"'
            '><tengigabitethernet><name>10/0/1</name><channel-group><mode>acti'
            've</mode><port-int>4</port-int><type>standard</type></channel-gro'
            'up></tengigabitethernet></interface></config>'
        )

        self.assertTrue(expected_xml, mock_callback.returned_data)
