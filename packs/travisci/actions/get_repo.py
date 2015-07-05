from lib.action import TravisCI


class GetRepoDetails(TravisCI):
    def run(self, repo):
        """
        Returns Details of given Repository
        """
        path = '/repos/' + str(repo)
        response = self._perform_request(path, method="GET")
        data = response.json()
        return data
