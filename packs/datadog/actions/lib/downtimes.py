from base import DatadogBaseAction
from datadog import api


class DatadogScheduleMonitorDowntime(DatadogBaseAction):
    def _run(self, **kwargs):
        return api.Downtime.create(**kwargs)
