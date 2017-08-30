import requests

from lib.base import OpscenterAction


class ListRequestsAction(OpscenterAction):
    def run(self, request_type, list_all=True, cluster_id=None):
        if not cluster_id:
            cluster_id = self.cluster_id

        url = self._get_full_url([cluster_id, 'request', request_type])

        return requests.get(url, params={'list_all': int(list_all)}).json()
