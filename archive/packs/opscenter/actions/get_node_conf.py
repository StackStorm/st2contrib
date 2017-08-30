import requests

from lib.base import OpscenterAction


class GetNodeConfAction(OpscenterAction):

    def run(self, node_ip, cluster_id=None):
        if not cluster_id:
            cluster_id = self.cluster_id

        url = self._get_full_url([cluster_id, 'nodeconf', node_ip])

        return requests.get(url).json()
