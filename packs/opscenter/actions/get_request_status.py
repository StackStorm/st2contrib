import requests

from lib.base import OpscenterAction


class GetRequestStausAction(OpscenterAction):
    def run(self, request_id):

        url = self._get_full_url(['request', request_id, 'status'])

        return requests.get(url).json()
