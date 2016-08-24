import xml.etree.ElementTree as ET
from st2tests.base import BaseActionTestCase

from interface_v6_nd_suppress_ra import interface_v6_nd_suppress_ra

__all__ = [
    'Testinterface_v6_nd_suppress_ra'
]


class MockCallback(object):
    returned_data = None

    def callback(self, call, **kwargs):
        xml_result = ET.tostring(call)
        self.returned_data = xml_result


class Testinterface_v6_nd_suppress_ra(BaseActionTestCase):
    action_cls = interface_v6_nd_suppress_ra

    def test_action(self):
        action = self.get_action_instance()
        mock_callback = MockCallback()
        kwargs = {
            'username': '',
            'rbridge_id': '224',
            'int_type': 'tengigabitethernet',
            'ip': '',
            'password': '',
            'port': '22',
            'name': '10/0/1',
            'test': True,
            'callback': mock_callback.callback
        }

        action.run(**kwargs)

        expected_xml = """<config><interface xmlns="urn:brocade.com:mgmt:brocade-interface"><tengigabitethernet><name>10/0/1</name><ipv6><ipv6-nd-ra xmlns="urn:brocade.com:mgmt:brocade-ipv6-nd-ra"><ipv6-intf-cmds><nd><suppress-ra><suppress-ra-all /></suppress-ra></nd></ipv6-intf-cmds></ipv6-nd-ra></ipv6></tengigabitethernet></interface></config>"""

        self.assertTrue(expected_xml, mock_callback.returned_data)
