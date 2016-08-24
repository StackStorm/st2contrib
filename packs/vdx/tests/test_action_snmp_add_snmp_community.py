import xml.etree.ElementTree as ET
from st2tests.base import BaseActionTestCase

from snmp_add_snmp_community import snmp_add_snmp_community

__all__ = [
    'Testsnmp_add_snmp_community'
]


class MockCallback(object):
    returned_data = None

    def callback(self, call, **kwargs):
        xml_result = ET.tostring(call)
        self.returned_data = xml_result


class Testsnmp_add_snmp_community(BaseActionTestCase):
    action_cls = snmp_add_snmp_community

    def test_action(self):
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

        expected_xml = """<config><snmp-server xmlns="urn:brocade.com:mgmt:brocade-snmp"><community><community>test</community></community></snmp-server></config>"""

        self.assertTrue(expected_xml, mock_callback.returned_data)
