import xml.etree.ElementTree as ET
from st2tests.base import BaseActionTestCase

from interface_lacp_timeout import interface_lacp_timeout

__all__ = [
    'Testinterface_lacp_timeout'
]


class MockCallback(object):
    returned_data = None

    def callback(self, call, **kwargs):
        xml_result = ET.tostring(call)
        self.returned_data = xml_result


class Testinterface_lacp_timeout(BaseActionTestCase):
    action_cls = interface_lacp_timeout

    def test_action(self):
        action = self.get_action_instance()
        mock_callback = MockCallback()
        kwargs = {
            'username': '',
            'lacp_timeout': 'short',
            'name': '10/0/5',
            'int_type': 'tengigabitethernet',
            'ip': '',
            'password': '',
            'port': '22',
            'test': True,
            'callback': mock_callback.callback
        }

        action.run(**kwargs)

        expected_xml = """<config><interface xmlns="urn:brocade.com:mgmt:brocade-interface"><tengigabitethernet><name>10/0/5</name><lacp xmlns="urn:brocade.com:mgmt:brocade-lacp"><timeout>short</timeout></lacp></tengigabitethernet></interface></config>"""

        self.assertTrue(expected_xml, mock_callback.returned_data)
