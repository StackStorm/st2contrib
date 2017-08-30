"""Generated test for checking pynos based actions
"""
import xml.etree.ElementTree as ET
from st2tests.base import BaseActionTestCase
from interface_trunk_mode import interface_trunk_mode

__all__ = [
    'TestInterfaceTrunkMode'
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


class TestInterfaceTrunkMode(BaseActionTestCase):
    """Test holder class
    """
    action_cls = interface_trunk_mode

    def test_action(self):
        """Generated test to check action
        """
        action = self.get_action_instance()
        mock_callback = MockCallback()
        kwargs = {
            'username': '',
            'name': '10/0/1',
            'int_type': 'tengigabitethernet',
            'ip': '',
            'password': '',
            'port': '22',
            'mode': 'trunk',
            'test': True,
            'callback': mock_callback.callback
        }

        action.run(**kwargs)

        expected_xml = (
            '<config><interface xmlns="urn:brocade.com:mgmt:brocade-interface"'
            '><tengigabitethernet><name>10/0/1</name><switchport><mode><vlan-m'
            'ode>trunk</vlan-mode></mode></switchport></tengigabitethernet></i'
            'nterface></config>'
        )

        self.assertTrue(expected_xml, mock_callback.returned_data)
