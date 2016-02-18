from st2tests.base import BaseActionTestCase

from parse_csv import ParseCSVAction

__all__ = [
    'ParseCSVActionTestCase'
]

MOCK_DATA_1 = """
first,last,year
name1,surename1,1990
""".strip()

MOCK_DATA_2 = """
first|last|year
name1|surename1|1990
""".strip()


class ParseCSVActionTestCase(BaseActionTestCase):
    action_cls = ParseCSVAction

    def test_run_comma_delimiter(self):
        result = self.get_action_instance().run(data=MOCK_DATA_1, delimiter=',')
        expected = [
            ['first', 'last', 'year'],
            ['name1', 'surename1', '1990']
        ]
        self.assertEqual(result, expected)

    def test_run_pipe_delimiter(self):
        result = self.get_action_instance().run(data=MOCK_DATA_2, delimiter='|')
        expected = [
            ['first', 'last', 'year'],
            ['name1', 'surename1', '1990']
        ]
        self.assertEqual(result, expected)
