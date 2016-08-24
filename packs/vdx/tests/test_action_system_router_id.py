import xml.etree.ElementTree as ET
from st2tests.base import BaseActionTestCase

from system_router_id import system_router_id

__all__ = [
    'Testsystem_router_id'
]


class MockCallback(object):
    returned_data = None

    def callback(self, call, **kwargs):
        xml_result = ET.tostring(call)
        self.returned_data = xml_result


class Testsystem_router_id(BaseActionTestCase):
    action_cls = system_router_id

    def test_action(self):
        action = self.get_action_instance()
        mock_callback = MockCallback()
        kwargs = {
            'router_id': '4',
            'username': '',
            'rbridge_id': '224',
            'ip': '',
            'password': '',
            'port': '22',
            'test': True,
            'callback': mock_callback.callback
        }

        action.run(**kwargs)

        expected_xml = """<config><rbridge-id xmlns="urn:brocade.com:mgmt:brocade-rbridge"><rbridge-id>224</rbridge-id><ip><rtm-config xmlns="urn:brocade.com:mgmt:brocade-rtm"><router-id>4</router-id></rtm-config></ip></rbridge-id></config>"""

        self.assertTrue(expected_xml, mock_callback.returned_data)
