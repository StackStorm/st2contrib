from lib.action import TravisCI
import yaml


class ListBuildsAction(TravisCI):
    def run(self, reponame, username):
        """
        Listing builds for a give Repository
        """
        uri = self.config['uri'] + '/repos/' + username + '/' + \
            reponame + '/builds'
        response = self._perform_request(uri, method="GET")
        data = yaml.load(response.content)
        builds = []
        for arg in data['builds']:
            builds.append({'build_id': arg['id'],
                          'commit_id': arg['commit_id']})
        for i in data['commits']:
            for b in builds:
                if b['commit_id'] == i['id']:
                    b['branch_name'] = 'branch'
        return builds
