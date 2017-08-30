import requests

from lib.base import OpscenterAction


class GetNodesInfoAction(OpscenterAction):

    def run(self, node_ip, node_property=None, cluster_id=None):
        if not cluster_id:
            cluster_id = self.cluster_id

        url_parts = [cluster_id, 'nodes', node_ip]

        if node_property:
            url_parts.extend(node_property)

        url = self._get_full_url(url_parts)

        return requests.get(url).json()
