"""Generated test for checking pynos based actions
"""
import xml.etree.ElementTree as ET
from st2tests.base import BaseActionTestCase
from bgp_neighbor import bgp_neighbor

__all__ = [
    'TestBgpNeighbor'
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


class TestBgpNeighbor(BaseActionTestCase):
    """Test holder class
    """
    action_cls = bgp_neighbor

    def test_action(self):
        """Generated test to check action
        """
        action = self.get_action_instance()
        mock_callback = MockCallback()
        kwargs = {
            'username': '',
            'ip_addr': '10.10.0.1/24',
            'rbridge_id': '224',
            'ip': '',
            'vrf': 'test',
            'remote_as': '18003',
            'password': '',
            'port': '22',
            'delete': False,
            'test': True,
            'callback': mock_callback.callback
        }

        action.run(**kwargs)

        expected_xml = (
            '<config><rbridge-id xmlns="urn:brocade.com:mgmt:brocade-rbridge">'
            '<rbridge-id>224</rbridge-id><router><bgp xmlns="urn:brocade.com:m'
            'gmt:brocade-bgp"><vrf-name>test</vrf-name><router-bgp-cmds-holder'
            '><router-bgp-attributes><neighbor-ips><neighbor-addr><router-bgp-'
            'neighbor-address>10.10.0.1</router-bgp-neighbor-address><remote-a'
            's>18003</remote-as></neighbor-addr></neighbor-ips></router-bgp-at'
            'tributes></router-bgp-cmds-holder></bgp></router></rbridge-id></c'
            'onfig>'
        )

        self.assertTrue(expected_xml, mock_callback.returned_data)
