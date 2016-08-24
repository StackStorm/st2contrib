import xml.etree.ElementTree as ET
from st2tests.base import BaseActionTestCase

from interface_transport_service import interface_transport_service

__all__ = [
    'Testinterface_transport_service'
]


class MockCallback(object):
    returned_data = None

    def callback(self, call, **kwargs):
        xml_result = ET.tostring(call)
        self.returned_data = xml_result


class Testinterface_transport_service(BaseActionTestCase):
    action_cls = interface_transport_service

    def test_action(self):
        action = self.get_action_instance()
        mock_callback = MockCallback()
        kwargs = {
            'username': '',
            'password': '',
            'service_id': '24',
            'ip': '',
            'vlan': '24',
            'port': '22',
            'test': True,
            'callback': mock_callback.callback
        }

        action.run(**kwargs)

        expected_xml = """<config><interface-vlan xmlns="urn:brocade.com:mgmt:brocade-interface"><interface><vlan><name>24</name><transport-service>24</transport-service></vlan></interface></interface-vlan></config>"""

        self.assertTrue(expected_xml, mock_callback.returned_data)
