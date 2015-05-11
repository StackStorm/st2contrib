from lib.action import St2BaseAction
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

        result = self._run_client_method(method=self.client.liveactions.query,
                                         method_kwargs=kwargs,
                                         format_func=format_client_list_result)
        return result
