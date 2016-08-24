import xml.etree.ElementTree as ET
from st2tests.base import BaseActionTestCase

from interface_trunk_allowed_vlan import interface_trunk_allowed_vlan

__all__ = [
    'Testinterface_trunk_allowed_vlan'
]


class MockCallback(object):
    returned_data = None

    def callback(self, call, **kwargs):
        xml_result = ET.tostring(call)
        self.returned_data = xml_result


class Testinterface_trunk_allowed_vlan(BaseActionTestCase):
    action_cls = interface_trunk_allowed_vlan

    def test_action(self):
        action = self.get_action_instance()
        mock_callback = MockCallback()
        kwargs = {
            'username': '',
            'ctag': '10-11',
            'name': '10/0/1',
            'ip': '',
            'vlan': '10',
            'int_type': 'tengigabitethernet',
            'action': 'add',
            'password': '',
            'port': '22',
            'test': True,
            'callback': mock_callback.callback
        }

        action.run(**kwargs)

        expected_xml = """<config><interface xmlns="urn:brocade.com:mgmt:brocade-interface"><tengigabitethernet><name>10/0/1</name><switchport><trunk><trunk-vlan-classification><allowed><vlan><add><trunk-vlan-id>10</trunk-vlan-id><trunk-ctag-range>10-11</trunk-ctag-range></add></vlan></allowed></trunk-vlan-classification></trunk></switchport></tengigabitethernet></interface></config>"""

        self.assertTrue(expected_xml, mock_callback.returned_data)
