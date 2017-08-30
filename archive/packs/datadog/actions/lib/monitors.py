from base import DatadogBaseAction
from datadog import api


class DatadogCreateMonitor(DatadogBaseAction):
    def _run(self, **kwargs):
        return api.Monitor.create(**kwargs)


class DatadogDeleteMonitor(DatadogBaseAction):
    def _run(self, **kwargs):
        return api.Monitor.delete(kwargs.pop("monitor_id"))


class DatadogEditMonitor(DatadogBaseAction):
    def _run(self, **kwargs):
        return api.Monitor.update(kwargs.pop("monitor_id"), **kwargs)


class DatadogAllMonitors(DatadogBaseAction):
    def _run(self):
        return api.Monitor.get_all()


class DatadogGetMonitor(DatadogBaseAction):
    def _run(self, **kwargs):
        return api.Monitor.get(kwargs.pop("monitor_id"), **kwargs)


class DatadogMuteAllMonitors(DatadogBaseAction):
    def _run(self):
        return api.Monitor.mute_all()


class DatadogMuteMonitor(DatadogBaseAction):
    def _run(self, **kwargs):
        return api.Monitor.mute(kwargs.pop("monitor_id"), **kwargs)


class DatadogUnmuteAllMonitors(DatadogBaseAction):
    def _run(self):
        return api.Monitor.unmute_all()


class DatadogUnmuteMonitor(DatadogBaseAction):
    def _run(self, **kwargs):
        return api.Monitor.unmute(kwargs.pop("monitor_id"), **kwargs)
