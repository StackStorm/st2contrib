import csv
from StringIO import StringIO

from st2actions.runners.pythonrunner import Action
from st2common.exceptions.action import InvalidActionParameterException

__all__ = [
    'FormatCSVAction'
]


class FormatCSVAction(Action):
    def run(self, data, delimiter=',', quote_char='"'):
        if len(data) == 0:
            raise InvalidActionParameterException("data has no rows")
        if not isinstance(data, list):
            raise InvalidActionParameterException("data must be a list")
        if not isinstance(data[0], dict):
            raise InvalidActionParameterException("data must be a list of dict")

        fieldnames = data[0].keys()
        sh = StringIO()
        writer = csv.DictWriter(sh, fieldnames=fieldnames)

        writer.writeheader()
        for row in data:
            writer.writerow(row)

        out = sh.getvalue()
        sh.close()
        return out
