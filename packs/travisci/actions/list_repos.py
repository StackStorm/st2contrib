from lib.action import TravisCI


class GetRepos(TravisCI):
    def run(self, username):
        """
        Listing all Repos for a given user
        """
        path = '/repos?owner_name=' + username
        response = self._perform_request(path, method="GET")
        data = response.json()
        repos = {}
        for repo in data:
            repos[repo['id']] = repo
        return repos
