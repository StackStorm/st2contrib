from lib.action import TravisCI
import requests
import json


class Hooks(TravisCI):
    def run(self, hookid, action=None):
        """
        Enable or Disable a hook to monitor through Travis
        """
        _HEADERS = self.travis
        _HEADERS['Authorization'] = self.config["Authorization"]
        _HEADERS['Content-Type'] = self.config["Content-Type"]
        uri = self.config["uri"] + '/hooks/' + str(hookid)
        json_req = {"hook": {"active": action}}
        json_req = json.dumps(json_req)
        response = requests.put(uri, data=json_req, headers=_HEADERS)
        return response.content
