import xml.etree.ElementTree as ET
from st2tests.base import BaseActionTestCase

from interface_private_vlan_type import interface_private_vlan_type

__all__ = [
    'Testinterface_private_vlan_type'
]


class MockCallback(object):
    returned_data = None

    def callback(self, call, **kwargs):
        xml_result = ET.tostring(call)
        self.returned_data = xml_result


class Testinterface_private_vlan_type(BaseActionTestCase):
    action_cls = interface_private_vlan_type

    def test_action(self):
        action = self.get_action_instance()
        mock_callback = MockCallback()
        kwargs = {
            'username': '',
            'name': '10',
            'pvlan_type': 'primary',
            'ip': '',
            'password': '',
            'port': '22',
            'test': True,
            'callback': mock_callback.callback
        }

        action.run(**kwargs)

        expected_xml = """<config><interface-vlan xmlns="urn:brocade.com:mgmt:brocade-interface"><interface><vlan><name>10</name><private-vlan><pvlan-type-leaf>primary</pvlan-type-leaf></private-vlan></vlan></interface></interface-vlan></config>"""

        self.assertTrue(expected_xml, mock_callback.returned_data)
