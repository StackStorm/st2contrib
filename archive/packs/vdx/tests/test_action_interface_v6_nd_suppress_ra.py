"""Generated test for checking pynos based actions
"""
import xml.etree.ElementTree as ET
from st2tests.base import BaseActionTestCase
from interface_v6_nd_suppress_ra import interface_v6_nd_suppress_ra

__all__ = [
    'TestInterfaceV6NdSuppressRa'
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


class TestInterfaceV6NdSuppressRa(BaseActionTestCase):
    """Test holder class
    """
    action_cls = interface_v6_nd_suppress_ra

    def test_action(self):
        """Generated test to check action
        """
        action = self.get_action_instance()
        mock_callback = MockCallback()
        kwargs = {
            'username': '',
            'rbridge_id': '224',
            'int_type': 'tengigabitethernet',
            'ip': '',
            'password': '',
            'port': '22',
            'name': '10/0/1',
            'test': True,
            'callback': mock_callback.callback
        }

        action.run(**kwargs)

        expected_xml = (
            '<config><interface xmlns="urn:brocade.com:mgmt:brocade-interface"'
            '><tengigabitethernet><name>10/0/1</name><ipv6><ipv6-nd-ra xmlns="'
            'urn:brocade.com:mgmt:brocade-ipv6-nd-ra"><ipv6-intf-cmds><nd><sup'
            'press-ra><suppress-ra-all /></suppress-ra></nd></ipv6-intf-cmds><'
            '/ipv6-nd-ra></ipv6></tengigabitethernet></interface></config>'
        )

        self.assertTrue(expected_xml, mock_callback.returned_data)
