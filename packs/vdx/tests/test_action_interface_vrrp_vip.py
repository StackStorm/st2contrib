import xml.etree.ElementTree as ET
from st2tests.base import BaseActionTestCase

from interface_vrrp_vip import interface_vrrp_vip

__all__ = [
    'Testinterface_vrrp_vip'
]


class MockCallback(object):
    returned_data = None

    def callback(self, call, **kwargs):
        xml_result = ET.tostring(call)
        self.returned_data = xml_result


class Testinterface_vrrp_vip(BaseActionTestCase):
    action_cls = interface_vrrp_vip

    def test_action(self):
        action = self.get_action_instance()
        mock_callback = MockCallback()
        kwargs = {
            'username': '',
            'rbridge_id': '224',
            'ip': '',
            'vrid': '10',
            'vip': '10.9.2.1',
            'int_type': 'gigabitethernet',
            'password': '',
            'port': '22',
            'name': '10/0/1',
            'test': True,
            'callback': mock_callback.callback
        }

        action.run(**kwargs)

        expected_xml = """<config><interface xmlns="urn:brocade.com:mgmt:brocade-interface"><gigabitethernet><name>10/0/1</name><vrrp xmlns="urn:brocade.com:mgmt:brocade-vrrp"><vrid>10</vrid><version>3</version><virtual-ip><virtual-ipaddr>10.9.2.1</virtual-ipaddr></virtual-ip></vrrp></gigabitethernet></interface></config>"""

        self.assertTrue(expected_xml, mock_callback.returned_data)
