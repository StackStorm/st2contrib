from base import DatadogBaseAction
from datadog import api


class DatadogPostCheckRun(DatadogBaseAction):
    def _run(self, **kwargs):
        return api.ServiceCheck.check(**kwargs)
