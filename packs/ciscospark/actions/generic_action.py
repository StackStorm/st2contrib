from lib.action import CiscoSparkAction

__all__ = [
    'GenericAction'
]


class GenericAction(CiscoSparkAction):

    def run(self, accessor, method_name, **kwargs):
        a = getattr(self.connection, accessor)
        result = getattr(a, method_name)(**kwargs)
        return self._parse_result(result)
