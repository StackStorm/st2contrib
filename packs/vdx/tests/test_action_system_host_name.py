import xml.etree.ElementTree as ET
from st2tests.base import BaseActionTestCase

from system_host_name import system_host_name

__all__ = [
    'Testsystem_host_name'
]


class MockCallback(object):
    returned_data = None

    def callback(self, call, **kwargs):
        xml_result = ET.tostring(call)
        self.returned_data = xml_result


class Testsystem_host_name(BaseActionTestCase):
    action_cls = system_host_name

    def test_action(self):
        action = self.get_action_instance()
        mock_callback = MockCallback()
        kwargs = {
            'username': '',
            'rbridge_id': '224',
            'get': 'False',
            'ip': '',
            'password': '',
            'port': '22',
            'host_name': 'test',
            'test': True,
            'callback': mock_callback.callback
        }

        action.run(**kwargs)

        expected_xml = """<config><rbridge-id xmlns="urn:brocade.com:mgmt:brocade-rbridge"><rbridge-id>224</rbridge-id><switch-attributes><host-name>test</host-name></switch-attributes></rbridge-id></config>"""

        self.assertTrue(expected_xml, mock_callback.returned_data)
