import requests

from lib.base import OpscenterAction


class DrainNodeAction(OpscenterAction):
    def run(self, node_ip, cluster_id=None):
        if not cluster_id:
            cluster_id = self.cluster_id

        url = self._get_full_url([cluster_id, 'ops', 'drain', node_ip])

        return requests.get(url).json()
