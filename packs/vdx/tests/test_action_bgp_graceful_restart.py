import xml.etree.ElementTree as ET
from st2tests.base import BaseActionTestCase

from bgp_graceful_restart import bgp_graceful_restart

__all__ = [
    'Testbgp_graceful_restart'
]


class MockCallback(object):
    returned_data = None

    def callback(self, call, **kwargs):
        xml_result = ET.tostring(call)
        self.returned_data = xml_result


class Testbgp_graceful_restart(BaseActionTestCase):
    action_cls = bgp_graceful_restart

    def test_action(self):
        action = self.get_action_instance()
        mock_callback = MockCallback()
        kwargs = {
            'username': '',
            'rbridge_id': '224',
            'get': 'False',
            'ip': '',
            'vrf': 'test',
            'password': '',
            'port': '22',
            'afi': 'ipv4',
            'test': True,
            'callback': mock_callback.callback
        }

        action.run(**kwargs)

        expected_xml = """<config><rbridge-id xmlns="urn:brocade.com:mgmt:brocade-rbridge"><rbridge-id>224</rbridge-id><router><bgp xmlns="urn:brocade.com:mgmt:brocade-bgp"><vrf-name>test</vrf-name><router-bgp-cmds-holder><address-family><ipv4><ipv4-unicast><af-common-cmds-holder><graceful-restart><graceful-restart-status /></graceful-restart></af-common-cmds-holder></ipv4-unicast></ipv4></address-family></router-bgp-cmds-holder></bgp></router></rbridge-id></config>"""

        self.assertTrue(expected_xml, mock_callback.returned_data)
