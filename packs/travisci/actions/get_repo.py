from lib.action import TravisCI


class GetRepoDetails(TravisCI):
    def run(self, repo_id):
        """
        Returns Details of given Repository
        """
        path = '/repos/' + str(repo_id)
        response = self._perform_request(path, method="GET")
        data = response.json()
        return data
