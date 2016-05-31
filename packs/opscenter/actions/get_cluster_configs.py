import requests

from lib.base import OpscenterAction


class GetClustersAction(OpscenterAction):

    def run(self):
        url = self._get_full_url(['cluster-configs'])

        return requests.get(url).json()
