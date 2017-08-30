from base import DatadogBaseAction
from datadog import api


class DatadogAddHostTags(DatadogBaseAction):
    def _run(self, **kwargs):
        return api.Tag.create(kwargs.pop("host"), **kwargs)


class DatadogGetHostTags(DatadogBaseAction):
    def _run(self, **kwargs):
        return api.Tag.get(kwargs.pop("host"))


class DatadogGetTags(DatadogBaseAction):
    def _run(self, **kwargs):
        return api.Tag.get_all(**kwargs)


class DatadogRemoveHostTags(DatadogBaseAction):
    def _run(self, **kwargs):
        return api.Tag.delete(kwargs.pop("host"), **kwargs)


class DatadogUpdateHostTags(DatadogBaseAction):
    def _run(self, **kwargs):
        return api.Tag.update(kwargs.pop("host"), **kwargs)
