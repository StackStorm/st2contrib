from st2actions.runners.pythonrunner import Action
from parsers import ResultSets
import pytesla


class BaseAction(Action):
    def __init__(self, config):
        super(BaseAction, self).__init__(config)
        self.connection = pytesla.Connection(config['tesla_username'],
                                             config['tesla_password'])
        self.formatter = ResultSets()
