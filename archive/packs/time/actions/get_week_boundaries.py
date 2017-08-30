import arrow

from st2common.util import isotime
from st2actions.runners.pythonrunner import Action


class GetWeekBoundariesTimestampsAction(Action):
    def run(self, date=None):
        if date:
            dt = isotime.parse(date)
            dt = arrow.get(dt)
        else:
            # No date provided, use current date
            dt = arrow.utcnow()

        start_timestamp = dt.floor('week').timestamp
        end_timestamp = dt.ceil('week').timestamp

        return start_timestamp, end_timestamp
