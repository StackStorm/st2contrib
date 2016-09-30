from base import DatadogBaseAction
from datadog import api


class DatadogSearch(DatadogBaseAction):
    def _run(self, **kwargs):
        return api.Infrastructure.search(**kwargs)
