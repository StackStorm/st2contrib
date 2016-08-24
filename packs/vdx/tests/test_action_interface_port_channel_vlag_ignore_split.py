import xml.etree.ElementTree as ET
from st2tests.base import BaseActionTestCase

from interface_port_channel_vlag_ignore_split import interface_port_channel_vlag_ignore_split

__all__ = [
    'Testinterface_port_channel_vlag_ignore_split'
]


class MockCallback(object):
    returned_data = None

    def callback(self, call, **kwargs):
        xml_result = ET.tostring(call)
        self.returned_data = xml_result


class Testinterface_port_channel_vlag_ignore_split(BaseActionTestCase):
    action_cls = interface_port_channel_vlag_ignore_split

    def test_action(self):
        action = self.get_action_instance()
        mock_callback = MockCallback()
        kwargs = {
            'username': '',
            'name': '1',
            'ip': '',
            'password': '',
            'enabled': 'True',
            'port': '22',
            'test': True,
            'callback': mock_callback.callback
        }

        action.run(**kwargs)

        expected_xml = """<config><interface xmlns="urn:brocade.com:mgmt:brocade-interface"><port-channel><name>1</name><vlag><ignore-split /></vlag></port-channel></interface></config>"""

        self.assertTrue(expected_xml, mock_callback.returned_data)
