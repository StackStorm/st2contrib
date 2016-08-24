"""Generated test for checking pynos based actions
"""
import xml.etree.ElementTree as ET
from st2tests.base import BaseActionTestCase
from interface_fabric_isl import interface_fabric_isl

__all__ = [
    'TestInterfaceFabricIsl'
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


class TestInterfaceFabricIsl(BaseActionTestCase):
    """Test holder class
    """
    action_cls = interface_fabric_isl

    def test_action(self):
        """Generated test to check action
        """
        action = self.get_action_instance()
        mock_callback = MockCallback()
        kwargs = {
            'username': '',
            'name': '10/0/2',
            'get': False,
            'ip': '',
            'enabled': True,
            'int_type': 'tengigabitethernet',
            'password': '',
            'port': '22',
            'test': True,
            'callback': mock_callback.callback
        }

        action.run(**kwargs)

        expected_xml = (
            '<config><interface xmlns="urn:brocade.com:mgmt:brocade-interface"'
            '><tengigabitethernet><name>10/0/2</name><fabric xmlns="urn:brocad'
            'e.com:mgmt:brocade-fcoe"><fabric-isl><fabric-isl-enable /></fabri'
            'c-isl></fabric></tengigabitethernet></interface></config>'
        )

        self.assertTrue(expected_xml, mock_callback.returned_data)
