from lib.action import TravisCI
import requests
import yaml


class GetRepos(TravisCI):
    def run(self, username):
        """
        Listing all Repos for a give user
        """
        _HEADERS = self.travis
        _HEADERS['Authorization'] = self.config["Authorization"]
        uri = self.config["uri"] + '/repos?owner_name=' + username
        response = requests.get(uri, headers=_HEADERS)
        data = yaml.load(response.content)
        repos = {}
        for arg in data['repos']:
            repos[arg['id']] = arg['slug']
        return repos
