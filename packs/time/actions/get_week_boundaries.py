import time
import datetime

from st2common.util import isotime
from st2actions.runners.pythonrunner import Action


class GetWeekBoundariesTimestampsAction(Action):
    def run(self, date=None):
        if date:
            dt = isotime.parse(date)
        else:
            dt = datetime.datetime.utcnow()

        start_dt = (dt - datetime.timedelta(days=dt.weekday()))
        end_dt = (start_dt + datetime.timedelta(days=6))
        start_dt = start_dt.replace(hour=0, minute=0, second=0, microsecond=0)
        end_dt = end_dt.replace(hour=23, minute=59, second=59, microsecond=0)

        start_timestamp = int(time.mktime(start_dt.timetuple()))
        end_timestamp = int(time.mktime(end_dt.timetuple()))

        return start_timestamp, end_timestamp
