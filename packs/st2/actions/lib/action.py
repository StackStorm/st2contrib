from st2actions.runners.pythonrunner import Action
from st2client.client import Client
from st2client.models.keyvalue import KeyValuePair  # pylint: disable=no-name-in-module

from lib.utils import filter_none_values


__all__ = [
    'St2BaseAction'
]


class St2BaseAction(Action):
    def __init__(self, config):
        super(St2BaseAction, self).__init__(config)
        self._client = Client
        self._kvp = KeyValuePair
        self.client = self._get_client()

    def _get_client(self):
        host = self.config['base_url']

        try:
            return self._client(base_url=host)
        except Exception as e:
            return e

    def _run_client_method(self, method, method_kwargs, format_func):
        """
        Run the provided client method and format the result.

        :param method: Client method to run.
        :type method: ``func``

        :param method_kwargs: Keyword arguments passed to the client method.
        :type method_kwargs: ``dict``

        :param format_func: Function for formatting the result.
        :type format_func: ``func``

        :rtype: ``list`` of ``dict``
        """
        # Filter out parameters with string value of "None"
        # This is a work around since the default values can only be strings
        method_kwargs = filter_none_values(method_kwargs)
        method_name = method.__name__
        self.logger.debug('Calling client method "%s" with kwargs "%s"' % (method_name,
                                                                           method_kwargs))

        result = method(**method_kwargs)
        result = format_func(result)
        return result
