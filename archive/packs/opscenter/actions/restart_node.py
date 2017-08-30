import json

import requests

from lib.base import OpscenterAction


class RestartNodeAction(OpscenterAction):
    def run(self, node_ip, cluster_id=None, drain_first=True,
            wait_for_thrift=True):
        if not cluster_id:
            cluster_id = self.cluster_id

        url = self._get_full_url([cluster_id, 'ops', 'restart', node_ip])

        payload = {
            'wait_for_thrift': wait_for_thrift,
            'drain_first': drain_first
        }

        return requests.post(url, data=json.dumps(payload)).json()
