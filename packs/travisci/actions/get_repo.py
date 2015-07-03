from lib.action import TravisCI
import requests
import yaml


class GetRepoDetails(TravisCI):
    def run(self, repo):
        """
        Returns Details of given Repository
        """
        uri = self.config['uri'] + '/repos/' + str(repo)
        response = self._perform_request(uri, method="GET")
        data = yaml.load(response.content)
        res = {}
	res = {
            'name': data['repo']['slug'], 
            'build_state': data['repo']['last_build_state'],\
            'github_language': data['repo']['github_language'],\
            'last_build_id': data['repo']['last_build_id']
        }
        return res
