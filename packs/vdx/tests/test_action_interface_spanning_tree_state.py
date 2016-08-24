import xml.etree.ElementTree as ET
from st2tests.base import BaseActionTestCase

from interface_spanning_tree_state import interface_spanning_tree_state

__all__ = [
    'Testinterface_spanning_tree_state'
]


class MockCallback(object):
    returned_data = None

    def callback(self, call, **kwargs):
        xml_result = ET.tostring(call)
        self.returned_data = xml_result


class Testinterface_spanning_tree_state(BaseActionTestCase):
    action_cls = interface_spanning_tree_state

    def test_action(self):
        action = self.get_action_instance()
        mock_callback = MockCallback()
        kwargs = {
            'username': '',
            'name': '10/0/1',
            'int_type': 'tengigabitethernet',
            'ip': '',
            'password': '',
            'enabled': True,
            'port': '22',
            'test': True,
            'callback': mock_callback.callback
        }

        action.run(**kwargs)

        expected_xml = """<config><interface xmlns="urn:brocade.com:mgmt:brocade-interface"><tengigabitethernet><name>10/0/1</name><spanning-tree xmlns="urn:brocade.com:mgmt:brocade-xstp"><shutdown operation="delete" /></spanning-tree></tengigabitethernet></interface></config>"""

        self.assertTrue(expected_xml, mock_callback.returned_data)
