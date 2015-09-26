import csv
from StringIO import StringIO

from st2actions.runners.pythonrunner import Action

__all__ = [
    'ParseCSVAction'
]


class ParseCSVAction(Action):
    def run(self, data, delimiter=',', quote_char='"'):
        fh = StringIO(data)

        reader = csv.reader(fh, delimiter=str(delimiter), quotechar=str(quote_char))

        result = []
        for row in reader:
            result.append(row)
        return result
