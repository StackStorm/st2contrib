import requests

from lib.base import OpscenterAction


class CancelRequestAction(OpscenterAction):
    def run(self, request_id):

        url = self._get_full_url(['request', request_id, 'cancel'])

        return requests.post(url).json()
