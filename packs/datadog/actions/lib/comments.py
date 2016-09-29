from base import DatadogBaseAction
from datadog import api


class DatadogCreateComment(DatadogBaseAction):
    def _run(self, **kwargs):
        return api.Comment.create(**kwargs)


class DatadogDeleteComment(DatadogBaseAction):
    def _run(self, **kwargs):
        return api.Comment.delete(kwargs.pop("comment_id"))


class DatadogEditComment(DatadogBaseAction):
    def _run(self, **kwargs):
        return api.Comment.update(kwargs.pop("comment_id"), **kwargs)
