
import time
import datetime

from lib.base import BaseGithubAction


class CreateDeploymentAction(BaseGithubAction):
    def run(self, api_user, repository, deployment_id, state, description):

        valid_states = ["pending", "success", "error", "failure"]

        if api_user:
            self.token = self._get_user_token(api_user)

        if state not in valid_states:
            raise ValueError("Invalid state: {}".format(state))

        payload = {"state": state,
                   "description": description}

        response = self._request("POST",
                                 "/repos/{}/deployments/{}/statuses".format(
                                     repository,
                                     deployment_id),
                                 payload,
                                 self.token)

        ts_created_at = time.mktime(
            datetime.datetime.strptime(
                response['created_at'],
                "%Y-%m-%dT%H:%M:%SZ").timetuple())

        ts_updated_at = time.mktime(
            datetime.datetime.strptime(
                response['updated_at'],
                "%Y-%m-%dT%H:%M:%SZ").timetuple())

        results = {'creator': response['creator']['login'],
                   'id': response['id'],
                   'url': response['url'],
                   'description': response['description'],
                   'repository_url': response['repository_url'],
                   'created_at': response['created_at'],
                   'updated_at': response['updated_at'],
                   'ts_created_at': ts_created_at,
                   'ts_updated_at': ts_updated_at}
        results['response'] = response

        return results
