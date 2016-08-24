import xml.etree.ElementTree as ET
from st2tests.base import BaseActionTestCase

from interface_port_channel_minimum_links import interface_port_channel_minimum_links

__all__ = [
    'Testinterface_port_channel_minimum_links'
]


class MockCallback(object):
    returned_data = None

    def callback(self, call, **kwargs):
        xml_result = ET.tostring(call)
        self.returned_data = xml_result


class Testinterface_port_channel_minimum_links(BaseActionTestCase):
    action_cls = interface_port_channel_minimum_links

    def test_action(self):
        action = self.get_action_instance()
        mock_callback = MockCallback()
        kwargs = {
            'username': '',
            'minimum_links': '2',
            'name': '1',
            'ip': '',
            'password': '',
            'port': '22',
            'test': True,
            'callback': mock_callback.callback
        }

        action.run(**kwargs)

        expected_xml = """<config><interface xmlns="urn:brocade.com:mgmt:brocade-interface"><port-channel><name>1</name><minimum-links>2</minimum-links></port-channel></interface></config>"""

        self.assertTrue(expected_xml, mock_callback.returned_data)
