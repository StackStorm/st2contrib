from _mssql import connect

from st2actions.runners.pythonrunner import Action

__all__ = [
    'MSSQLAction'
]


class MSSQLAction(Action):

    def __init__(self, config):
        super(MSSQLAction, self).__init__(config=config)
        self.config = config

    def connect(self, database=None, server=None, user=None, password=None):
        return connect(**self._connect_params(database, server, user, password))

    def _connect_params(self, database=None, server=None, user=None, password=None):
        database = database or self.config.get('default')
        db_config = self.config.get(database, {})
        params = {
            'database': db_config.get('database') or database,
            'server': server or db_config.get('server'),
            'user': user or db_config.get('user'),
            'password': password or db_config.get('password')
        }
        unspecified = [param for param, value in params.iteritems() if value is None]
        if unspecified:
            raise Exception("Must specify or configure in config.yaml: %s" % ', '.join(unspecified))
        return params
