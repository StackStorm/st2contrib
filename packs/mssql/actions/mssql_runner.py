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

    # pack action maps to PyMSSQL driver and ResultsProcessor handler
    ACTION_DRIVER_PROCESSOR_MAPPING = {
        'execute_insert': ('execute_non_query', 'execute_insert')
    }

    def __init__(self, config):
        super(MSSQLRunner, self).__init__(config)
        self.processor = ResultsProcessor(self.config)

    def run(self, action, query_string, params=None, server=None, user=None, password=None, database=None):
        try:
            # action corresponds to a pair of _mssql and ResultsProcessor methods
            driver_action, processor_action = self.ACTION_DRIVER_PROCESSOR_MAPPING.get(action, (action, action))
            with self.connect(server, user, password, database) as cursor:
                response = getattr(cursor, driver_action)(query_string, ast.literal_eval(params) if params else None)
                return getattr(self.processor, processor_action)(response, cursor)
        except MSSQLException as e:
            self.logger.error(e)
            sys.exit(1)
