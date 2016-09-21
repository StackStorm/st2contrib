
from lib.base import BaseGithubAction


class ListDeploymentsAction(BaseGithubAction):
    def run(self, api_user, repository):
        results = []

        if api_user:
            self.token = self._get_user_token(api_user)

        response = self._request("GET",
                                 "/repos/{}/deployments".format(repository),
                                 None,
                                 self.token)

        for dep in response:
            results.append(
                {'creator': dep['creator']['login'],
                 'statuses_url': dep['statuses_url'],
                 'repository_url': dep['repository_url'],
                 'ref': dep['ref'],
                 'task': dep['task'],
                 'payload': dep['payload'],
                 'environment': dep['environment'],
                 'description': dep['description'],
                 'created_at': dep['created_at'],
                 'updated_at': dep['updated_at']})

        return results
