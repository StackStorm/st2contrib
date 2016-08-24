import xml.etree.ElementTree as ET
from st2tests.base import BaseActionTestCase

from interface_proxy_arp import interface_proxy_arp

__all__ = [
    'Testinterface_proxy_arp'
]


class MockCallback(object):
    returned_data = None

    def callback(self, call, **kwargs):
        xml_result = ET.tostring(call)
        self.returned_data = xml_result


class Testinterface_proxy_arp(BaseActionTestCase):
    action_cls = interface_proxy_arp

    def test_action(self):
        action = self.get_action_instance()
        mock_callback = MockCallback()
        kwargs = {
            'username': '',
            'name': '10/0/2',
            'ip': '',
            'enabled': True,
            'int_type': 'tengigabitethernet',
            'password': '',
            'port': '22',
            'rbridge_id': '224',
            'test': True,
            'callback': mock_callback.callback
        }

        action.run(**kwargs)

        expected_xml = """<config><interface xmlns="urn:brocade.com:mgmt:brocade-interface"><tengigabitethernet><name>10/0/2</name><ip><ip-config xmlns="urn:brocade.com:mgmt:brocade-ip-config"><proxy-arp /></ip-config></ip></tengigabitethernet></interface></config>"""

        self.assertTrue(expected_xml, mock_callback.returned_data)
