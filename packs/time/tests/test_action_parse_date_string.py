import datetime

from st2tests.base import BaseActionTestCase

from lib.utils import dt_to_timestamp
from parse_date_string import ParseDateStringAction


class ParseDateStringActionTestCase(BaseActionTestCase):
    action_cls = ParseDateStringAction

    def test_run_success(self):
        action = self.get_action_instance()

        result = action.run(date_string='now')
        expected = datetime.datetime.utcnow()
        expected = dt_to_timestamp(expected)
        self.assertTimestampMatchesWithDrift(result, expected)

        result = action.run(date_string='1 hour ago')
        expected = (datetime.datetime.utcnow() - datetime.timedelta(hours=1))
        expected = dt_to_timestamp(expected)
        self.assertTimestampMatchesWithDrift(result, expected)

        result = action.run(date_string='3 days ago')
        expected = (datetime.datetime.utcnow() - datetime.timedelta(days=3))
        expected = dt_to_timestamp(expected)
        self.assertTimestampMatchesWithDrift(result, expected)

        # TODO: Uupstream library is broke, fix it
        # result = action.run(date_string='2013-05-12')
        # expected = datetime.datetime(2013, 5, 12)
        # expected = dt_to_timestamp(expected)
        # self.assertTimestampMatchesWithDrift(result, expected)

    def test_run_invalid_date_string(self):
        action = self.get_action_instance()
        self.assertRaises(ValueError, action.run, date_string='some invalid string')

    def assertTimestampMatches(self, actual_ts, expected_ts):
        """
        Custom function which asserts that the provided two timestamp match.
        """
        actual_ts = datetime.datetime.fromtimestamp(actual_ts)
        expected_ts = datetime.datetime.fromtimestamp(expected_ts)

        self.assertEqual(actual_ts, expected_ts)

    def assertTimestampMatchesWithDrift(self, actual_ts, expected_ts):
        """
        Custom assert function which allows actual result to drift from the expected one
        for +/- 1 second (this is to account for the time between the function runs).

        In addition to that, microseconds are stripped as well.
        """
        expected_timestamps = [expected_ts, (expected_ts + 1), (expected_ts - 1)]
        self.assertTrue(actual_ts in expected_timestamps)
