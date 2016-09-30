from base import DatadogBaseAction
from datadog import api


class DatadogPostTSPoints(DatadogBaseAction):
    def _run(self, **kwargs):
        return api.Metric.send(kwargs.pop("series"), **kwargs)


class DatadogQueryTSPoints(DatadogBaseAction):
    def _run(self, **kwargs):
        return api.Metric.query(**kwargs)
