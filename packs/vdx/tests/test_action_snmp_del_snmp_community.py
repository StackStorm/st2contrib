"""Generated test for checking pynos based actions
"""
import xml.etree.ElementTree as ET
from st2tests.base import BaseActionTestCase
from snmp_del_snmp_community import snmp_del_snmp_community

__all__ = [
    'TestSnmpDelSnmpCommunity'
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


class TestSnmpDelSnmpCommunity(BaseActionTestCase):
    """Test holder class
    """
    action_cls = snmp_del_snmp_community

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
            'community': 'community_test',
            'test': True,
            'callback': mock_callback.callback
        }

        action.run(**kwargs)

        expected_xml = (
            '<config><snmp-server xmlns="urn:brocade.com:mgmt:brocade-snmp"><c'
            'ommunity operation="delete"><community>community_test</community>'
            '</community></snmp-server></config>'
        )

        self.assertTrue(expected_xml, mock_callback.returned_data)
