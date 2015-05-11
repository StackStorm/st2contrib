from lib.action import St2BaseAction
from lib.formatters import format_client_list_result

__all__ = [
    'St2SensorsListAction'
]


class St2SensorsListAction(St2BaseAction):
    def run(self, pack=None):
        kwargs = {}

        if pack:
            kwargs['pack'] = pack

        result = self._run_client_method(method=self.client.sensors.get_all,
                                         method_kwargs=kwargs,
                                         format_func=format_client_list_result)
        return result
