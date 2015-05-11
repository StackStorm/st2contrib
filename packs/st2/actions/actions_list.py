from lib.action import St2BaseAction
from lib.formatters import format_client_list_result

__all__ = [
    'St2ActionsListAction'
]


class St2ActionsListAction(St2BaseAction):
    def run(self, pack=None):
        kwargs = {}

        if pack:
            kwargs['pack'] = pack

        result = self._run_client_method(method=self.client.actions.get_all,
                                         method_kwargs=kwargs,
                                         format_func=format_client_list_result)
        return result
