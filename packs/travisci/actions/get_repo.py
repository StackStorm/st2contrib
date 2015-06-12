from lib.action import TravisCI
import requests
import yaml


class GetRepoDetails(TravisCI):
    def run(self, repo):
        """
        Returns Details of given Repository
        """
        _HEADERS = self.travis
        uri = self.config['uri'] + '/repos/' + str(repo)
        response = requests.get(uri, headers=_HEADERS)
        data = yaml.load(response.content)
        res = {'name': data['repo']['slug'],
               'build_state': data['repo']['last_build_state'],
               'github_language': data['repo']['github_language'],
               'last_build_id': data['repo']['last_build_id'], }
        return res
