import xml.etree.ElementTree as ET
from st2tests.base import BaseActionTestCase

from interface_add_vlan_int import interface_add_vlan_int

__all__ = [
    'Testinterface_add_vlan_int'
]


class MockCallback(object):
    returned_data = None

    def callback(self, call, **kwargs):
        xml_result = ET.tostring(call)
        self.returned_data = xml_result


class Testinterface_add_vlan_int(BaseActionTestCase):
    action_cls = interface_add_vlan_int

    def test_action(self):
        action = self.get_action_instance()
        mock_callback = MockCallback()
        kwargs = {
            'username': '',
            'ip': '',
            'password': '',
            'port': '22',
            'vlan_id': '44',
            'test': True,
            'callback': mock_callback.callback
        }

        action.run(**kwargs)

        expected_xml = """<config><interface-vlan xmlns="urn:brocade.com:mgmt:brocade-interface"><interface><vlan><name>44</name></vlan></interface></interface-vlan></config>"""

        self.assertTrue(expected_xml, mock_callback.returned_data)
