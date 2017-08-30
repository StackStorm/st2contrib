from base import DatadogBaseAction
from datadog import api


class DatadogMuteHost(DatadogBaseAction):
    def _run(self, **kwargs):
        return api.Host.mute(kwargs.pop("host"), **kwargs)


class DatadogUnmuteHost(DatadogBaseAction):
    def _run(self, **kwargs):
        return api.Host.unmute(kwargs.pop("host"))
