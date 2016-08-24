import xml.etree.ElementTree as ET
from st2tests.base import BaseActionTestCase

from bgp_update_source import bgp_update_source

__all__ = [
    'Testbgp_update_source'
]


class MockCallback(object):
    returned_data = None

    def callback(self, call, **kwargs):
        xml_result = ET.tostring(call)
        self.returned_data = xml_result


class Testbgp_update_source(BaseActionTestCase):
    action_cls = bgp_update_source

    def test_action(self):
        action = self.get_action_instance()
        mock_callback = MockCallback()
        kwargs = {
            'username': '',
            'int_name': '1',
            'neighbor': '10.2.1.4',
            'get': 'False',
            'ip': '',
            'vrf': 'test',
            'int_type': 'tengigabitethernet',
            'password': '',
            'port': '22',
            'rbridge_id': '224',
            'test': True,
            'callback': mock_callback.callback
        }

        action.run(**kwargs)

        expected_xml = """<config><rbridge-id xmlns="urn:brocade.com:mgmt:brocade-rbridge"><rbridge-id>224</rbridge-id><router><bgp xmlns="urn:brocade.com:mgmt:brocade-bgp"><vrf-name>test</vrf-name><router-bgp-cmds-holder><router-bgp-attributes><neighbor-ips><neighbor-addr><router-bgp-neighbor-address>10.2.1.4</router-bgp-neighbor-address><update-source><loopback>1</loopback></update-source></neighbor-addr></neighbor-ips></router-bgp-attributes></router-bgp-cmds-holder></bgp></router></rbridge-id></config>"""

        self.assertTrue(expected_xml, mock_callback.returned_data)
