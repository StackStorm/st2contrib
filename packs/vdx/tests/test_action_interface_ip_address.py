import xml.etree.ElementTree as ET
from st2tests.base import BaseActionTestCase

from interface_ip_address import interface_ip_address

__all__ = [
    'Testinterface_ip_address'
]


class MockCallback(object):
    returned_data = None

    def callback(self, call, **kwargs):
        xml_result = ET.tostring(call)
        self.returned_data = xml_result


class Testinterface_ip_address(BaseActionTestCase):
    action_cls = interface_ip_address

    def test_action(self):
        action = self.get_action_instance()
        mock_callback = MockCallback()
        kwargs = {
            'username': '',
            'delete': 'False',
            'ip_addr': '10.10.0.1/24',
            'name': '10/0/1',
            'ip': '',
            'int_type': 'tengigabitethernet',
            'password': '',
            'port': '22',
            'rbridge_id': '224',
            'test': True,
            'callback': mock_callback.callback
        }

        action.run(**kwargs)

        expected_xml = """<config><interface xmlns="urn:brocade.com:mgmt:brocade-interface"><tengigabitethernet><name>10/0/1</name><ip><ip-config xmlns="urn:brocade.com:mgmt:brocade-ip-config"><address><address>10.10.0.1/24</address></address></ip-config></ip></tengigabitethernet></interface></config>"""

        self.assertTrue(expected_xml, mock_callback.returned_data)
