from abc import ABCMeta, abstractmethod
from datadog import initialize
from st2actions.runners.pythonrunner import Action


class DatadogBaseAction(Action):
    __metaclass__ = ABCMeta

    def __init__(self, config):
        super(DatadogBaseAction, self).__init__(config)
        self._init_dd()

    def _init_dd(self):
        options = {
            'api_key': self.config['api_key'],
            'app_key': self.config['app_key']
        }
        initialize(**options)

    @abstractmethod
    def _run(self, **kwargs):
        pass

    def run(self, **kwargs):
        # Removing empty strings, None from kwargs without excluding 0
        args = {k: v for k, v in kwargs.iteritems()
                if str(v).strip() and v is not None}
        out = self._run(**args)
        errors = out.get("errors")
        if errors:
            return (False, errors)
        return (True, out)
