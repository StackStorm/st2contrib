import json

from lib.action import TravisCI


class DisableHookAction(TravisCI):
    def run(self, hookid):
        """
        Disable a hook to monitor through Travis
        """
        path = '/hooks/' + str(hookid)
        json_req = {
            'hook': {
                'active': 'false'
            }
        }
        json_req = json.dumps(json_req)
        response = self._perform_request(path, data=json_req, method='PUT')
        return response.content
