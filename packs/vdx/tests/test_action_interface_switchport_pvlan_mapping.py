import xml.etree.ElementTree as ET
from st2tests.base import BaseActionTestCase

from interface_switchport_pvlan_mapping import interface_switchport_pvlan_mapping

__all__ = [
    'Testinterface_switchport_pvlan_mapping'
]


class MockCallback(object):
    returned_data = None

    def callback(self, call, **kwargs):
        xml_result = ET.tostring(call)
        self.returned_data = xml_result


class Testinterface_switchport_pvlan_mapping(BaseActionTestCase):
    action_cls = interface_switchport_pvlan_mapping

    def test_action(self):
        action = self.get_action_instance()
        mock_callback = MockCallback()
        kwargs = {
            'username': '',
            'sec_vlan': '10',
            'name': '10/0/2',
            'pri_vlan': '20',
            'int_type': 'tengigabitethernet',
            'ip': '',
            'password': '',
            'port': '22',
            'test': True,
            'callback': mock_callback.callback
        }

        action.run(**kwargs)

        expected_xml = """<config><interface xmlns="urn:brocade.com:mgmt:brocade-interface"><gigabitethernet><name>10/0/2</name><switchport><private-vlan><mapping><promis-pri-pvlan>20</promis-pri-pvlan><promis-sec-pvlan-range>10</promis-sec-pvlan-range></mapping></private-vlan></switchport></gigabitethernet></interface></config>"""

        self.assertTrue(expected_xml, mock_callback.returned_data)
