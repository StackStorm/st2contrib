from lib.action import TravisCI
import requests
import yaml


class GetBranches(TravisCI):
    def run(self, repo_id):
        """
        Listing branches for a give Repository
        """
        _HEADERS = self.travis
        uri = self.config["uri"] + '/repos/' + str(repo_id) + '/branches'
        response = requests.get(uri, headers=_HEADERS)
        data = yaml.load(response.content)
        branches = []
        for arg in data['commits']:
            branches.append(arg['branch'])
        return branches
