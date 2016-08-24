import xml.etree.ElementTree as ET
from st2tests.base import BaseActionTestCase

from interface_acc_vlan import interface_acc_vlan

__all__ = [
    'Testinterface_acc_vlan'
]


class MockCallback(object):
    returned_data = None

    def callback(self, call, **kwargs):
        xml_result = ET.tostring(call)
        self.returned_data = xml_result


class Testinterface_acc_vlan(BaseActionTestCase):
    action_cls = interface_acc_vlan

    def test_action(self):
        action = self.get_action_instance()
        mock_callback = MockCallback()
        kwargs = {
            'username': '',
            'password': '',
            'name': '10/0/2',
            'int_type': 'tengigabitethernet',
            'ip': '',
            'vlan': '10',
            'port': '22',
            'test': True,
            'callback': mock_callback.callback
        }

        action.run(**kwargs)

        expected_xml = """<config><interface xmlns="urn:brocade.com:mgmt:brocade-interface"><tengigabitethernet><name>10/0/2</name><switchport><access><accessvlan>10</accessvlan></access></switchport></tengigabitethernet></interface></config>"""

        self.assertTrue(expected_xml, mock_callback.returned_data)
