import xml.etree.ElementTree as ET
from st2tests.base import BaseActionTestCase

from interface_remove_port_channel import interface_remove_port_channel

__all__ = [
    'Testinterface_remove_port_channel'
]


class MockCallback(object):
    returned_data = None

    def callback(self, call, **kwargs):
        xml_result = ET.tostring(call)
        self.returned_data = xml_result


class Testinterface_remove_port_channel(BaseActionTestCase):
    action_cls = interface_remove_port_channel

    def test_action(self):
        action = self.get_action_instance()
        mock_callback = MockCallback()
        kwargs = {
            'username': '',
            'ip': '',
            'password': '',
            'port': '22',
            'port_int': '3',
            'test': True,
            'callback': mock_callback.callback
        }

        action.run(**kwargs)

        expected_xml = """<config><interface xmlns="urn:brocade.com:mgmt:brocade-interface"><port-channel operation="delete"><name>3</name></port-channel></interface></config>"""

        self.assertTrue(expected_xml, mock_callback.returned_data)
