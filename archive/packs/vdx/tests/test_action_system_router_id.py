"""Generated test for checking pynos based actions
"""
import xml.etree.ElementTree as ET
from st2tests.base import BaseActionTestCase
from system_router_id import system_router_id

__all__ = [
    'TestSystemRouterId'
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


class TestSystemRouterId(BaseActionTestCase):
    """Test holder class
    """
    action_cls = system_router_id

    def test_action(self):
        """Generated test to check action
        """
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

        expected_xml = (
            '<config><rbridge-id xmlns="urn:brocade.com:mgmt:brocade-rbridge">'
            '<rbridge-id>224</rbridge-id><ip><rtm-config xmlns="urn:brocade.co'
            'm:mgmt:brocade-rtm"><router-id>4</router-id></rtm-config></ip></r'
            'bridge-id></config>'
        )

        self.assertTrue(expected_xml, mock_callback.returned_data)
