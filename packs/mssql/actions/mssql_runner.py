from _mssql import MSSQLException
import ast
import sys

from lib.mssql_action import MSSQLAction
from lib.results_processor import ResultsProcessor


class MSSQLRunner(MSSQLAction):
    """
    Sends an action to MS SQL Server. An exception is logged on failure.

    The query_string accepts Python formatting. Please see README for details.
    """

    # Pack actions map to a pair of methods: PyMSSQL (_mssql) driver and ResultsProcessor handler
    ACTION_MAPPING = {
        'execute_insert': ('execute_non_query', 'execute_insert')
        # default: (action_name, action_name)
    }

    def __init__(self, config):
        super(MSSQLRunner, self).__init__(config)
        self.processor = ResultsProcessor(self.config, self.logger)

    def run(self, action, query_string, params=None,
            database=None, server=None, user=None, password=None):
        try:
            # action corresponds to a pair of _mssql and ResultsProcessor methods
            driver_action, processor_action = self.ACTION_MAPPING.get(action, (action, action))
            with self.connect(database, server, user, password) as cursor:
                params = ast.literal_eval(params) if params else None
                response = getattr(cursor, driver_action)(query_string, params)
                return getattr(self.processor, processor_action)(response, cursor)
        except MSSQLException as e:
            self.logger.error(e)
            sys.exit(1)
