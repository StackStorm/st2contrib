import requests

from lib.base import OpscenterAction


class GetNodesInfoAction(OpscenterAction):

    def run(self, cluster_id=None):
        if not cluster_id:
            cluster_id = self.cluster_id

        url = self._get_full_url([cluster_id, 'nodes'])

        return requests.get(url).json()
