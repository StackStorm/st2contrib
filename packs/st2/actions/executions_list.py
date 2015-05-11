from lib.action import St2BaseAction
from lib.utils import filter_none_values
from lib.formatters import format_client_list_result

__all__ = [
    'St2ExecutionsListAction'
]


class St2ExecutionsListAction(St2BaseAction):
    def run(self, action=None, status=None):
        kwargs = {}

        if action:
            kwargs['action'] = action

        if status:
            kwargs['status'] = status

        # Filter out parameters with string value of "None"
        # This is a work around since the default values can only be strings
        kwargs = filter_none_values(kwargs)

        if kwargs:
            method = self.client.liveactions.query
        else:
            method = self.client.liveactions.get_all

        result = self._run_client_method(method=method,
                                         method_kwargs=kwargs,
                                         format_func=format_client_list_result)
        return result
