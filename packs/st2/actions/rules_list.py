from lib.action import St2BaseAction
from lib.formatters import format_client_list_result

__all__ = [
    'St2RulesListAction'
]

EXCLUDE_ATTRIBUTES = [
    'trigger',
    'criteria',
    'action'
]


def format_result(result):
    return format_client_list_result(result=result, exclude_attributes=EXCLUDE_ATTRIBUTES)


class St2RulesListAction(St2BaseAction):
    def run(self, pack=None, limit=10):
        kwargs = {}
        kwargs['limit'] = limit

        if pack:
            kwargs['pack'] = pack

        result = self._run_client_method(method=self.client.rules.get_all,
                                         method_kwargs=kwargs,
                                         format_func=format_result)
        return result
