from lib.action import CiscoSparkAction

__all__ = [
    'GenericAction'
]


class GenericAction(CiscoSparkAction):

    def run(self, accessor, method_name, **kwargs):
        a = getattr(self.connection, accessor)
        result = getattr(a, method_name)(**kwargs)
        if method_name == 'list':
            result = list(result)  # iterate generator
        if isinstance(result, list):
            return [x._json for x in result]  # pylint: disable=no-member
        else:
            return result._json  # pylint: disable=no-member
