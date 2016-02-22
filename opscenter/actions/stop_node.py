import json

import requests

from lib.base import OpscenterAction


class StopNodeAction(OpscenterAction):
    def run(self, node_ip, cluster_id=None, drain_node=True):
        if not cluster_id:
            cluster_id = self.cluster_id

        payload = {'drain_first': drain_node}

        url = self._get_full_url([cluster_id, 'ops', 'stop', node_ip])

        return requests.post(url, data=json.dumps(payload)).json()
