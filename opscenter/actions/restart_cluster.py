import json

import requests

from lib.base import OpscenterAction


class RestartClusterAction(OpscenterAction):
    def run(self, cluster_id=None, drain_first=True, sleep_interval=60,
            ips=None):

        if not cluster_id:
            cluster_id = self.cluster_id

        url = self._get_full_url([cluster_id, 'ops', 'restart'])

        payload = {
            'drain_first': drain_first,
            'sleep': sleep_interval,
        }

        if ips:
            payload['ips'] = ips

        return requests.post(url, data=json.dumps(payload)).json()
