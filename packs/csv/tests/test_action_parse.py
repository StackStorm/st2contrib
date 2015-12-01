import unittest2

from parse_csv import ParseCSVAction

__all__ = [
    'ParseCSVActionTestCase'
]

MOCK_DATA = """
first,last,year
name1,surename1,1990
""".strip()

class ParseCSVActionTestCase(unittest2.TestCase):
    def test_run(self):
        result = ParseCSVAction().run(data=MOCK_DATA, delimiter=',')
        expected = [
            ['first', 'last', 'year'],
            ['name1', 'surename1', '1990']
        ]
        self.assertEqual(result, expected)
