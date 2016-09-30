from base import DatadogBaseAction
from datadog import api


class DatadogCreateScreenboard(DatadogBaseAction):
    def _run(self, **kwargs):
        return api.Screenboard.create(**kwargs)


class DatadogDeleteScreenboard(DatadogBaseAction):
    def _run(self, **kwargs):
        return api.Screenboard.delete(kwargs.pop("board_id"))


class DatadogGetallScreenboards(DatadogBaseAction):
    def _run(self):
        return api.Screenboard.get_all()


class DatadogGetScreenboard(DatadogBaseAction):
    def _run(self, **kwargs):
        return api.Screenboard.get(kwargs.pop("board_id"))


class DatadogRevokeSharedScreenboard(DatadogBaseAction):
    def _run(self, **kwargs):
        return api.Screenboard.revoke(kwargs.pop("board_id"))


class DatadogShareScreenboard(DatadogBaseAction):
    def _run(self, **kwargs):
        return api.Screenboard.share(kwargs.pop("board_id"))


class DatadogUpdateScreenboard(DatadogBaseAction):
    def _run(self, **kwargs):
        return api.Screenboard.update(kwargs.pop("board_id"), **kwargs)
