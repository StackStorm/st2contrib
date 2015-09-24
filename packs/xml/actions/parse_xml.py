import json

import xmltodict

from st2actions.runners.pythonrunner import Action

__all__ = [
    'ParseXMLAction'
]


class ParseXMLAction(Action):
    def run(self, data):
        result = xmltodict.parse(data)
        result = json.dumps(result)
        return result
