import json
from datadog import api
from base import DatadogBaseAction


class DatadogCreateEmbed(DatadogBaseAction):
    def _run(self, **kwargs):
        return api.Embed.create(graph_json=json.dumps(kwargs.pop("graph")),
                                **kwargs)


class DatadogEnableEmbed(DatadogBaseAction):
    def _run(self, **kwargs):
        return api.Embed.enable(kwargs.get("embed_id"))


class DatadogGetAllEmbeds(DatadogBaseAction):
    def _run(self):
        return api.Embed.get_all()


class DatadogGetEmbed(DatadogBaseAction):
    def _run(self, **kwargs):
        return api.Embed.get(kwargs.pop("embed_id"), **kwargs)


class DatadogRevokeEmbed(DatadogBaseAction):
    def _run(self, **kwargs):
        return api.Embed.revoke(kwargs.get("embed_id"))
