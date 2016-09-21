
import time
import datetime

from lib.base import BaseGithubAction


class CreateDeploymentAction(BaseGithubAction):
    def run(self, api_user, repository, description, payload,
            ref="master", environment="production", task="deploy"):

        if api_user:
            self.token = self._get_user_token(api_user)

        payload = {"ref": ref,
                   "task": task,
                   "payload": payload,
                   "environment": environment,
                   "description": description}

        response = self._request("POST",
                                 "/repos/{}/deployments".format(repository),
                                 payload,
                                 self.token)

        ts_created_at = time.mktime(
            datetime.datetime.strptime(
                response['created_at'],
                "%Y-%m-%dT%H:%M:%SZ").timetuple())

        results = {'creator': response['creator']['login'],
                   'id': response['id'],
                   'sha': response['sha'],
                   'url': response['url'],
                   'ref': response['ref'],
                   'task': response['task'],
                   'payload': response['payload'],
                   'environment': response['environment'],
                   'description': response['description'],
                   'statuses_url': response['statuses_url'],
                   'repository_url': response['repository_url'],
                   'created_at': response['created_at'],
                   'updated_at': response['updated_at'],
                   'ts_created_at': ts_created_at}
        results['response'] = response

        return results
