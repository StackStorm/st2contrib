from lib.action import TravisCI
import requests
import yaml


class GetRepos(TravisCI):
    def run(self, username):
        """
        Listing all Repos for a give user
        """
        uri = self.config["uri"]+'/repos?owner_name='+username
        response = self._perform_request(uri, method="GET")
        data = yaml.load(response.content)
        repos = {}
        for arg in data['repos']:
            repos[arg['id']] = arg['slug']
        return repos
