
import time
import datetime

from lib.base import BaseGithubAction


class GetDeploymentStatusesAction(BaseGithubAction):
    def run(self, api_user, repository, deployment_id):

        if api_user:
            self.token = self._get_user_token(api_user)

        payload = {"id": deployment_id}

        responses = self._request("GET",
                                  "/repos/{}/deployments/{}/statuses".format(
                                      repository, deployment_id),
                                  payload,
                                  self.token)
        results = []
        for response in responses:
            ts_created_at = time.mktime(
                datetime.datetime.strptime(
                    response['created_at'],
                    "%Y-%m-%dT%H:%M:%SZ").timetuple())

            results.append({'creator': response['creator']['login'],
                            'id': response['id'],
                            'description': response['description'],
                            'state': response['state'],
                            'target_url': response['target_url'],
                            'created_at': response['created_at'],
                            'updated_at': response['updated_at'],
                            'ts_created_at': ts_created_at})

        return results
