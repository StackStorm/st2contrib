from lib.action import TravisCI
import yaml


class GetRepos(TravisCI):
    def run(self, username):
        """
        Listing all Repos for a given user
        """
        path = '/repos?owner_name=' + username
        response = self._perform_request(path, method="GET")
        data = yaml.load(response.content)
        repos = {}
        for arg in data['repos']:
            repos[arg['id']] = arg['slug']
        return repos
