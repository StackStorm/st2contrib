import xml.etree.ElementTree as ET
from st2tests.base import BaseActionTestCase

from bgp_remove_bgp import bgp_remove_bgp

__all__ = [
    'Testbgp_remove_bgp'
]


class MockCallback(object):
    returned_data = None

    def callback(self, call, **kwargs):
        xml_result = ET.tostring(call)
        self.returned_data = xml_result


class Testbgp_remove_bgp(BaseActionTestCase):
    action_cls = bgp_remove_bgp

    def test_action(self):
        action = self.get_action_instance()
        mock_callback = MockCallback()
        kwargs = {
            'username': '',
            'rbridge_id': '224',
            'ip': '',
            'password': '',
            'port': '22',
            'vrf': 'test',
            'test': True,
            'callback': mock_callback.callback
        }

        action.run(**kwargs)

        expected_xml = """<config><rbridge-id xmlns="urn:brocade.com:mgmt:brocade-rbridge"><rbridge-id>224</rbridge-id><router><bgp operation="delete" xmlns="urn:brocade.com:mgmt:brocade-bgp"><vrf-name>test</vrf-name></bgp></router></rbridge-id></config>"""

        self.assertTrue(expected_xml, mock_callback.returned_data)
