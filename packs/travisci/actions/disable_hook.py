from lib.action import TravisCI
import json


class DisableHookAction(TravisCI):
    def run(self, hookid):
        """
        Disable a hook to monitor through Travis
        """
        uri = self.config["uri"] + '/hooks/' + str(hookid)
        json_req = {
            "hook": {
                "active": "false"}
        }
        json_req = json.dumps(json_req)
        response = self._perform_request(uri, data=json_req, method="PUT")
        return response.content
