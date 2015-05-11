from lib.action import St2BaseAction
from lib.utils import filter_none_values
from lib.formatters import format_client_list_result

__all__ = [
    'St2RulesListAction'
]


class St2RulesListAction(St2BaseAction):
    def run(self, pack=None):
        kwargs = {}

        if pack:
            kwargs['pack'] = pack

        # Filter out parameters with string value of "None"
        # This is a work around since the default values can only be strings
        kwargs = filter_none_values(kwargs)
        result = self._run_client_method(method=self.client.rules.get_all,
                                         method_kwargs=kwargs,
                                         format_func=format_client_list_result)
        return result
