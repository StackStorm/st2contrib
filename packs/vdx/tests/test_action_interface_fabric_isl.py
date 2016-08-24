import xml.etree.ElementTree as ET
from st2tests.base import BaseActionTestCase

from interface_fabric_isl import interface_fabric_isl

__all__ = [
    'Testinterface_fabric_isl'
]


class MockCallback(object):
    returned_data = None

    def callback(self, call, **kwargs):
        xml_result = ET.tostring(call)
        self.returned_data = xml_result


class Testinterface_fabric_isl(BaseActionTestCase):
    action_cls = interface_fabric_isl

    def test_action(self):
        action = self.get_action_instance()
        mock_callback = MockCallback()
        kwargs = {
            'username': '',
            'name': '10/0/2',
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

        expected_xml = """<config><interface xmlns="urn:brocade.com:mgmt:brocade-interface"><tengigabitethernet><name>10/0/2</name><fabric xmlns="urn:brocade.com:mgmt:brocade-fcoe"><fabric-isl><fabric-isl-enable /></fabric-isl></fabric></tengigabitethernet></interface></config>"""

        self.assertTrue(expected_xml, mock_callback.returned_data)
