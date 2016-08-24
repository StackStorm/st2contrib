import xml.etree.ElementTree as ET
from st2tests.base import BaseActionTestCase

from interface_fabric_trunk import interface_fabric_trunk

__all__ = [
    'Testinterface_fabric_trunk'
]


class MockCallback(object):
    returned_data = None

    def callback(self, call, **kwargs):
        xml_result = ET.tostring(call)
        self.returned_data = xml_result


class Testinterface_fabric_trunk(BaseActionTestCase):
    action_cls = interface_fabric_trunk

    def test_action(self):
        action = self.get_action_instance()
        mock_callback = MockCallback()
        kwargs = {
            'username': '',
            'name': '10/0/1',
            'get': False,
            'ip': '',
            'enabled': True,
            'int_type': 'tengigabitethernet',
            'password': '',
            'port': '22',
            'test': True,
            'callback': mock_callback.callback
        }

        action.run(**kwargs)

        expected_xml = """<config><interface xmlns="urn:brocade.com:mgmt:brocade-interface"><tengigabitethernet><name>10/0/1</name><fabric xmlns="urn:brocade.com:mgmt:brocade-fcoe"><fabric-trunk><fabric-trunk-enable /></fabric-trunk></fabric></tengigabitethernet></interface></config>"""

        self.assertTrue(expected_xml, mock_callback.returned_data)
