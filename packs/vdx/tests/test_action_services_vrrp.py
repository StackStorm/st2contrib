"""Generated test for checking pynos based actions
"""
import xml.etree.ElementTree as ET
from st2tests.base import BaseActionTestCase
from services_vrrp import services_vrrp

__all__ = [
    'TestServicesVrrp'
]


class MockCallback(object):  # pylint:disable=too-few-public-methods
    """Class to hold mock callback and result
    """
    returned_data = None

    def callback(self, call, **kwargs):  # pylint:disable=unused-argument
        """Mock callback method
        """
        xml_result = ET.tostring(call)
        self.returned_data = xml_result


class TestServicesVrrp(BaseActionTestCase):
    """Test holder class
    """
    action_cls = services_vrrp

    def test_action(self):
        """Generated test to check action
        """
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

        expected_xml = (
            '<config><rbridge-id xmlns="urn:brocade.com:mgmt:brocade-rbridge">'
            '<rbridge-id>1</rbridge-id><protocol xmlns="urn:brocade.com:mgmt:b'
            'rocade-interface"><hide-vrrp-holder xmlns="urn:brocade.com:mgmt:b'
            'rocade-vrrp"><vrrp /></hide-vrrp-holder></protocol></rbridge-id><'
            '/config>'
        )

        self.assertTrue(expected_xml, mock_callback.returned_data)
