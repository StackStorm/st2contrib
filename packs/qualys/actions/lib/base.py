from qualysapi.connector import QGConnector

from st2actions.runners.pythonrunner import Action

__all__ = [
    'QualysBaseAction',
]


class QualysBaseAction(Action):
    def __init__(self, config):
        super(QualysBaseAction, self).__init__(config)
        self.connection = QGConnector(
            (config['username'],
             config['password']),
            config['hostname']
        )
