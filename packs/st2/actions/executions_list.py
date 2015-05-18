from lib.action import St2BaseAction
from lib.formatters import format_client_list_result

__all__ = [
    'St2ExecutionsListAction'
]

EXCLUDE_ATTRIBUTES = [
    'trigger',
    'trigger_type',
    'trigger_instance',
    'liveaction',
    'context'
]


def format_result(result):
    return format_client_list_result(result=result, exclude_attributes=EXCLUDE_ATTRIBUTES)


class St2ExecutionsListAction(St2BaseAction):
    def run(self, action=None, status=None, limit=5):
        kwargs = {}

        kwargs['limit'] = limit

        if action:
            kwargs['action'] = action

        if status:
            kwargs['status'] = status

        if kwargs:
            method = self.client.liveactions.query
        else:
            method = self.client.liveactions.get_all

        result = self._run_client_method(method=method,
                                         method_kwargs=kwargs,
                                         format_func=format_result)
        return result
