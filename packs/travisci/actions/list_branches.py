from lib.action import TravisCI
import yaml


class ListBranchesAction(TravisCI):
    def run(self, repo_id):
        """
        Listing branches for a give Repository
        """
        path = '/repos/' + str(repo_id) + '/branches'
        response = self._perform_request(path, method="GET")
        data = yaml.load(response.content)
        branches = []
        for arg in data['commits']:
            branches.append(arg['branch'])
        return branches
