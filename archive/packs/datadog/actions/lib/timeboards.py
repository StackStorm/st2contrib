from base import DatadogBaseAction
from datadog import api


class DatadogCreateTimeboard(DatadogBaseAction):
    def _run(self, **kwargs):
        return api.Timeboard.create(**kwargs)


class DatadogDeleteTimeboard(DatadogBaseAction):
    def _run(self, **kwargs):
        return api.Timeboard.delete(kwargs.pop("board_id"))


class DatadogGetAllTimeboards(DatadogBaseAction):
    def _run(self):
        return api.Timeboard.get_all()


class DatadogGetTimeboard(DatadogBaseAction):
    def _run(self, **kwargs):
        return api.Timeboard.get(kwargs.pop("board_id"))


class DatadogUpdateTimeboard(DatadogBaseAction):
    def _run(self, **kwargs):
        return api.Timeboard.update(kwargs.pop("board_id"), **kwargs)
