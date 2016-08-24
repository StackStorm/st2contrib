import xml.etree.ElementTree as ET
from st2tests.base import BaseActionTestCase

from bgp_multihop import bgp_multihop

__all__ = [
    'Testbgp_multihop'
]


class MockCallback(object):
    returned_data = None

    def callback(self, call, **kwargs):
        xml_result = ET.tostring(call)
        self.returned_data = xml_result


class Testbgp_multihop(BaseActionTestCase):
    action_cls = bgp_multihop

    def test_action(self):
        action = self.get_action_instance()
        mock_callback = MockCallback()
        kwargs = {
            'count': '3',
            'username': '',
            'rbridge_id': '224',
            'get': 'False',
            'ip': '',
            'vrf': 'test',
            'neighbor': '10.0.2.1',
            'password': '',
            'port': '22',
            'test': True,
            'callback': mock_callback.callback
        }

        action.run(**kwargs)

        expected_xml = """<config><rbridge-id xmlns="urn:brocade.com:mgmt:brocade-rbridge"><rbridge-id>224</rbridge-id><router><bgp xmlns="urn:brocade.com:mgmt:brocade-bgp"><vrf-name>test</vrf-name><router-bgp-cmds-holder><router-bgp-attributes><neighbor-ips><neighbor-addr><router-bgp-neighbor-address>10.0.2.1</router-bgp-neighbor-address><ebgp-multihop><ebgp-multihop-count>3</ebgp-multihop-count></ebgp-multihop></neighbor-addr></neighbor-ips></router-bgp-attributes></router-bgp-cmds-holder></bgp></router></rbridge-id></config>"""

        self.assertTrue(expected_xml, mock_callback.returned_data)
