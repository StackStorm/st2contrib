import xml.etree.ElementTree as ET
from st2tests.base import BaseActionTestCase

from interface_del_access_vlan import interface_del_access_vlan

__all__ = [
    'Testinterface_del_access_vlan'
]


class MockCallback(object):
    returned_data = None

    def callback(self, call, **kwargs):
        xml_result = ET.tostring(call)
        self.returned_data = xml_result


class Testinterface_del_access_vlan(BaseActionTestCase):
    action_cls = interface_del_access_vlan

    def test_action(self):
        action = self.get_action_instance()
        mock_callback = MockCallback()
        kwargs = {
            'username': '',
            'password': '',
            'inter_type': 'tengigabitethernet',
            'ip': '',
            'inter': '10/0/1',
            'port': '22',
            'vlan_id': '44',
            'test': True,
            'callback': mock_callback.callback
        }

        action.run(**kwargs)

        expected_xml = """<config><interface xmlns="urn:brocade.com:mgmt:brocade-interface"><tengigabitethernet><name>10/0/1</name><switchport><access><accessvlan operation="delete">44</accessvlan></access></switchport></tengigabitethernet></interface></config>"""

        self.assertTrue(expected_xml, mock_callback.returned_data)
