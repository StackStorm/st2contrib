from st2tests.base import BaseActionTestCase

from parse_xml import ParseXMLAction

__all__ = [
    'ParseXMLActionTestCase'
]

MOCK_DATA_1 = """
<note>
<to>Tove</to>
<from>Jani</from>
<heading>Reminder</heading>
<body>Don't forget me this weekend!</body>
</note>
""".strip()


class ParseXMLActionTestCase(BaseActionTestCase):
    action_cls = ParseXMLAction

    def test_run(self):
        result = self.get_action_instance().run(data=MOCK_DATA_1)
        expected = {
            'note': {
                'to': 'Tove',
                'from': 'Jani',
                'heading': 'Reminder',
                'body': 'Don\'t forget me this weekend!'
            }
        }
        self.assertEqual(result, expected)
