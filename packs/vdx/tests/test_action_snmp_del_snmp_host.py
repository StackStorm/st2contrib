import xml.etree.ElementTree as ET
from st2tests.base import BaseActionTestCase

from snmp_del_snmp_host import snmp_del_snmp_host

__all__ = [
    'Testsnmp_del_snmp_host'
]


class MockCallback(object):
    returned_data = None

    def callback(self, call, **kwargs):
        xml_result = ET.tostring(call)
        self.returned_data = xml_result


class Testsnmp_del_snmp_host(BaseActionTestCase):
    action_cls = snmp_del_snmp_host

    def test_action(self):
        action = self.get_action_instance()
        mock_callback = MockCallback()
        kwargs = {
            'username': '',
            'host_info': ['10.0.2.1', '135'],
            'ip': '',
            'password': '',
            'port': '22',
            'community': 'test',
            'test': True,
            'callback': mock_callback.callback
        }

        action.run(**kwargs)

        expected_xml = """<config><snmp-server xmlns="urn:brocade.com:mgmt:brocade-snmp"><host operation="delete"><ip>10.0.2.1</ip><community>test</community><udp-port>135</udp-port></host></snmp-server></config>"""

        self.assertTrue(expected_xml, mock_callback.returned_data)
