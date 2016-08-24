import xml.etree.ElementTree as ET
from st2tests.base import BaseActionTestCase

from interface_vlan_pvlan_association_add import interface_vlan_pvlan_association_add

__all__ = [
    'Testinterface_vlan_pvlan_association_add'
]


class MockCallback(object):
    returned_data = None

    def callback(self, call, **kwargs):
        xml_result = ET.tostring(call)
        self.returned_data = xml_result


class Testinterface_vlan_pvlan_association_add(BaseActionTestCase):
    action_cls = interface_vlan_pvlan_association_add

    def test_action(self):
        action = self.get_action_instance()
        mock_callback = MockCallback()
        kwargs = {
            'username': '',
            'sec_vlan': '45',
            'name': '10',
            'ip': '',
            'password': '',
            'port': '22',
            'test': True,
            'callback': mock_callback.callback
        }

        action.run(**kwargs)

        expected_xml = """<config><interface-vlan xmlns="urn:brocade.com:mgmt:brocade-interface"><interface><vlan><name>10</name><private-vlan><association><sec-assoc-add>45</sec-assoc-add></association></private-vlan></vlan></interface></interface-vlan></config>"""

        self.assertTrue(expected_xml, mock_callback.returned_data)
