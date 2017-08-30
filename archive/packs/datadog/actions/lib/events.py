from base import DatadogBaseAction
from datadog import api


class DatadogGetEvent(DatadogBaseAction):
    def _run(self, **kwargs):
        return api.Event.get(kwargs.pop("event_id"))


class DatadogPostEvent(DatadogBaseAction):
    def _run(self, **kwargs):
        return api.Event.create(**kwargs)


class DatadogQueryEvent(DatadogBaseAction):
    def _run(self, **kwargs):
        return api.Event.query(**kwargs)
