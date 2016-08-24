import xml.etree.ElementTree as ET
from st2tests.base import BaseActionTestCase

from interface_admin_state import interface_admin_state

__all__ = [
    'Testinterface_admin_state'
]


class MockCallback(object):
    returned_data = None

    def callback(self, call, **kwargs):
        xml_result = ET.tostring(call)
        self.returned_data = xml_result


class Testinterface_admin_state(BaseActionTestCase):
    action_cls = interface_admin_state

    def test_action(self):
        action = self.get_action_instance()
        mock_callback = MockCallback()
        kwargs = {
            'username': '',
            'name': '10/0/1',
            'ip': '',
            'enabled': True,
            'int_type': 'tengigabitethernet',
            'password': '',
            'port': '22',
            'rbridge_id': '224',
            'test': True,
            'callback': mock_callback.callback
        }

        action.run(**kwargs)

        expected_xml = """<config><interface xmlns="urn:brocade.com:mgmt:brocade-interface"><tengigabitethernet><name>10/0/1</name><shutdown operation="delete" /></tengigabitethernet></interface></config>"""

        self.assertTrue(expected_xml, mock_callback.returned_data)
