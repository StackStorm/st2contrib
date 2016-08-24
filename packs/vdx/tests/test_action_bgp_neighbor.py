import xml.etree.ElementTree as ET
from st2tests.base import BaseActionTestCase

from bgp_neighbor import bgp_neighbor

__all__ = [
    'Testbgp_neighbor'
]


class MockCallback(object):
    returned_data = None

    def callback(self, call, **kwargs):
        xml_result = ET.tostring(call)
        self.returned_data = xml_result


class Testbgp_neighbor(BaseActionTestCase):
    action_cls = bgp_neighbor

    def test_action(self):
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
            'delete': 'False',
            'test': True,
            'callback': mock_callback.callback
        }

        action.run(**kwargs)

        expected_xml = """<config><rbridge-id xmlns="urn:brocade.com:mgmt:brocade-rbridge"><rbridge-id>224</rbridge-id><router><bgp xmlns="urn:brocade.com:mgmt:brocade-bgp"><vrf-name>test</vrf-name><router-bgp-cmds-holder><router-bgp-attributes><neighbor-ips><neighbor-addr><router-bgp-neighbor-address>10.10.0.1</router-bgp-neighbor-address><remote-as>18003</remote-as></neighbor-addr></neighbor-ips></router-bgp-attributes></router-bgp-cmds-holder></bgp></router></rbridge-id></config>"""

        self.assertTrue(expected_xml, mock_callback.returned_data)
