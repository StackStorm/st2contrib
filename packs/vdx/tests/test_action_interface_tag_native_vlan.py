import xml.etree.ElementTree as ET
from st2tests.base import BaseActionTestCase

from interface_tag_native_vlan import interface_tag_native_vlan

__all__ = [
    'Testinterface_tag_native_vlan'
]


class MockCallback(object):
    returned_data = None

    def callback(self, call, **kwargs):
        xml_result = ET.tostring(call)
        self.returned_data = xml_result


class Testinterface_tag_native_vlan(BaseActionTestCase):
    action_cls = interface_tag_native_vlan

    def test_action(self):
        action = self.get_action_instance()
        mock_callback = MockCallback()
        kwargs = {
            'username': '',
            'name': '10/0/1',
            'ip': '',
            'enabled': True,
            'mode': 'trunk',
            'int_type': 'tengigabitethernet',
            'password': '',
            'port': '22',
            'test': True,
            'callback': mock_callback.callback
        }

        action.run(**kwargs)

        expected_xml = """<config><interface xmlns="urn:brocade.com:mgmt:brocade-interface"><tengigabitethernet><name>10/0/1</name><switchport><trunk><tag><native-vlan /></tag></trunk></switchport></tengigabitethernet></interface></config>"""

        self.assertTrue(expected_xml, mock_callback.returned_data)
