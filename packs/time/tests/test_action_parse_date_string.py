import datetime

import arrow

from st2tests.base import BaseActionTestCase

from parse_date_string import ParseDateStringAction


class ParseDateStringActionTestCase(BaseActionTestCase):
    def test_run_success(self):
        action = ParseDateStringAction()

        result = action.run(date_string='now')
        expected = arrow.utcnow().timestamp
        self.assertTrue(result in [expected, (expected + 1), (expected - 1)])

        result = action.run(date_string='1 hour ago')
        expected = arrow.utcnow().replace(hours=-1).timestamp
        self.assertEqual(result, expected)

        result = action.run(date_string='3 days ago')
        expected = arrow.utcnow().replace(days=-3).timestamp
        self.assertEqual(result, expected)

        result = action.run(date_string='2013-05-12')
        expected = datetime.datetime(2013, 5, 12)
        expected = arrow.get(expected).timestamp
        self.assertEqual(result, expected)

    def test_run_invalid_date_string(self):
        action = ParseDateStringAction()
        self.assertRaises(ValueError, action.run, date_string='some invalid string')
