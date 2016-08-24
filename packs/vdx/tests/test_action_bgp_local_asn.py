import xml.etree.ElementTree as ET
from st2tests.base import BaseActionTestCase

from bgp_local_asn import bgp_local_asn

__all__ = [
    'Testbgp_local_asn'
]


class MockCallback(object):
    returned_data = None

    def callback(self, call, **kwargs):
        xml_result = ET.tostring(call)
        self.returned_data = xml_result


class Testbgp_local_asn(BaseActionTestCase):
    action_cls = bgp_local_asn

    def test_action(self):
        action = self.get_action_instance()
        mock_callback = MockCallback()
        kwargs = {
            'username': '',
            'rbridge_id': '224',
            'get': 'False',
            'ip': '',
            'local_as': '44322',
            'vrf': 'test',
            'password': '',
            'port': '22',
            'test': True,
            'callback': mock_callback.callback
        }

        action.run(**kwargs)

        expected_xml = """<config><rbridge-id xmlns="urn:brocade.com:mgmt:brocade-rbridge"><rbridge-id>224</rbridge-id><router><bgp xmlns="urn:brocade.com:mgmt:brocade-bgp"><vrf-name>test</vrf-name><router-bgp-cmds-holder><router-bgp-attributes><local-as>44322</local-as></router-bgp-attributes></router-bgp-cmds-holder></bgp></router></rbridge-id></config>"""

        self.assertTrue(expected_xml, mock_callback.returned_data)
