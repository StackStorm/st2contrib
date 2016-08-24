"""Generated test for checking pynos based actions
"""
import xml.etree.ElementTree as ET
from st2tests.base import BaseActionTestCase
from snmp_add_snmp_community import snmp_add_snmp_community

__all__ = [
    'TestSnmpAddSnmpCommunity'
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


class TestSnmpAddSnmpCommunity(BaseActionTestCase):
    """Test holder class
    """
    action_cls = snmp_add_snmp_community

    def test_action(self):
        """Generated test to check action
        """
        action = self.get_action_instance()
        mock_callback = MockCallback()
        kwargs = {
            'username': '',
            'ip': '',
            'password': '',
            'port': '22',
            'community': 'test',
            'test': True,
            'callback': mock_callback.callback
        }

        action.run(**kwargs)

        expected_xml = (
            '<config><snmp-server xmlns="urn:brocade.com:mgmt:brocade-snmp"><c'
            'ommunity><community>test</community></community></snmp-server></c'
            'onfig>'
        )

        self.assertTrue(expected_xml, mock_callback.returned_data)
