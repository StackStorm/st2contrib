from lib.action import TravisCI
import requests
import yaml


class GetBuilds(TravisCI):
    def run(self, reponame, username):
        """
        Listing builds for a give Repository
        """
        _HEADERS = self.travis
        uri = self.config['uri'] + '/repos/' + username + '/' + \
            reponame + '/builds'
        response = requests.get(uri, headers=_HEADERS)
        data = yaml.load(response.content)
        builds = []
        for arg in data['builds']:
            builds.append(
                {'build_id': arg['id'], 'commit_id': arg['commit_id']}
            )
        for i in data['commits']:
            for b in builds:
                if b['commit_id'] == i['id']:
                    b['branch_name'] = i['branch']
        return builds
