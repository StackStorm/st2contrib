from base import DatadogBaseAction
from datadog import api


class DatadogGraphSnapshot(DatadogBaseAction):
    def _run(self, **kwargs):
        return api.Graph.create(**kwargs)
