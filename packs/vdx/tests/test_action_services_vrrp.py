import xml.etree.ElementTree as ET
from st2tests.base import BaseActionTestCase

from services_vrrp import services_vrrp

__all__ = [
    'Testservices_vrrp'
]


class MockCallback(object):
    returned_data = None

    def callback(self, call, **kwargs):
        xml_result = ET.tostring(call)
        self.returned_data = xml_result


class Testservices_vrrp(BaseActionTestCase):
    action_cls = services_vrrp

    def test_action(self):
        action = self.get_action_instance()
        mock_callback = MockCallback()
        kwargs = {
            'ip_version': '4',
            'ip': '',
            'username': '',
            'password': '',
            'port': '22',
            'test': True,
            'callback': mock_callback.callback
        }

        action.run(**kwargs)

        expected_xml = """<config><rbridge-id xmlns="urn:brocade.com:mgmt:brocade-rbridge"><rbridge-id>1</rbridge-id><protocol xmlns="urn:brocade.com:mgmt:brocade-interface"><hide-vrrp-holder xmlns="urn:brocade.com:mgmt:brocade-vrrp"><vrrp /></hide-vrrp-holder></protocol></rbridge-id></config>"""

        self.assertTrue(expected_xml, mock_callback.returned_data)
