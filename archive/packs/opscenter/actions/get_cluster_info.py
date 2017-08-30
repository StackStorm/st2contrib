import requests

from lib.base import OpscenterAction


class GetClusterInfoAction(OpscenterAction):

    def run(self, cluster_id=None, cluster_property=None):
        if not cluster_id:
            cluster_id = self.cluster_id

        url_parts = [cluster_id, 'cluster']

        if cluster_property:
            url_parts.extend(cluster_property)

        url = self._get_full_url(url_parts)

        return requests.get(url).json()
