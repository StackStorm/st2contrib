import json

from lib.action import TravisCI


class EnableHookAction(TravisCI):
    def run(self, hook_id):
        """
        Enable a hook to monitor through Travis
        """
        path = '/hooks/' + str(hook_id)
        json_req = {
            'hook': {
                'active': 'true'
            }
        }
        json_req = json.dumps(json_req)
        response = self._perform_request(path, data=json_req, method='PUT')
        return response.content
