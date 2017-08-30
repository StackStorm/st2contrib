import time

import dateparser

from st2actions.runners.pythonrunner import Action


class ParseDateStringAction(Action):
    def run(self, date_string):
        dt = dateparser.parse(date_string)

        if not dt:
            raise ValueError('Failed to parse date string: %s' % (date_string))

        timestamp = int(time.mktime(dt.timetuple()))
        return timestamp
