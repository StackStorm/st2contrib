"""Generated test for checking pynos based actions
"""
import xml.etree.ElementTree as ET
from st2tests.base import BaseActionTestCase
from interface_acc_vlan import interface_acc_vlan

__all__ = [
    'TestInterfaceAccVlan'
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


class TestInterfaceAccVlan(BaseActionTestCase):
    """Test holder class
    """
    action_cls = interface_acc_vlan

    def test_action(self):
        """Generated test to check action
        """
        action = self.get_action_instance()
        mock_callback = MockCallback()
        kwargs = {
            'username': '',
            'password': '',
            'name': '10/0/2',
            'int_type': 'tengigabitethernet',
            'ip': '',
            'vlan': '10',
            'port': '22',
            'test': True,
            'callback': mock_callback.callback
        }

        action.run(**kwargs)

        expected_xml = (
            '<config><interface xmlns="urn:brocade.com:mgmt:brocade-interface"'
            '><tengigabitethernet><name>10/0/2</name><switchport><access><acce'
            'ssvlan>10</accessvlan></access></switchport></tengigabitethernet>'
            '</interface></config>'
        )

        self.assertTrue(expected_xml, mock_callback.returned_data)
