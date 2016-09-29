from base import DatadogBaseAction
from datadog import api


class DatadogCreateUser(DatadogBaseAction):
    def _run(self, **kwargs):
        return api.User.create(**kwargs)


class DatadogDisableUser(DatadogBaseAction):
    def _run(self, **kwargs):
        return api.User.delete(kwargs.pop("user"))


class DatadogGetAllUsers(DatadogBaseAction):
    def _run(self):
        return api.User.get_all()


class DatadogGetUser(DatadogBaseAction):
    def _run(self, **kwargs):
        return api.User.get(kwargs.pop("handle"))


class DatadogUpdateUser(DatadogBaseAction):
    def _run(self, **kwargs):
        return api.User.update(kwargs.pop("handle"), **kwargs)
