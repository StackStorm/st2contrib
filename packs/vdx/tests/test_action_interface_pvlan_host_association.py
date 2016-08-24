import xml.etree.ElementTree as ET
from st2tests.base import BaseActionTestCase

from interface_pvlan_host_association import interface_pvlan_host_association

__all__ = [
    'Testinterface_pvlan_host_association'
]


class MockCallback(object):
    returned_data = None

    def callback(self, call, **kwargs):
        xml_result = ET.tostring(call)
        self.returned_data = xml_result


class Testinterface_pvlan_host_association(BaseActionTestCase):
    action_cls = interface_pvlan_host_association

    def test_action(self):
        action = self.get_action_instance()
        mock_callback = MockCallback()
        kwargs = {
            'username': '',
            'sec_vlan': '43',
            'name': '10/0/1',
            'pri_vlan': '10',
            'int_type': 'tengigabitethernet',
            'ip': '',
            'password': '',
            'port': '22',
            'test': True,
            'callback': mock_callback.callback
        }

        action.run(**kwargs)

        expected_xml = """<config><interface xmlns="urn:brocade.com:mgmt:brocade-interface"><tengigabitethernet><name>10/0/1</name><switchport><private-vlan><host-association><host-pri-pvlan>10</host-pri-pvlan><host-sec-pvlan>43</host-sec-pvlan></host-association></private-vlan></switchport></tengigabitethernet></interface></config>"""

        self.assertTrue(expected_xml, mock_callback.returned_data)
