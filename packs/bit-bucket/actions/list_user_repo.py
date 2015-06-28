from lib.action import BitBucket
import yaml


class ListReposAction(BitBucket):
    def run(self):
        """
        Listing repositories for a user, just execute it.
        It assumes that you have already places the name
        and password in config file. It returns repo's
        name, its state, its state, scm and private status.
        """
        url = self.config['Host'] + 'user/repositories/'
        response = self._perform_request(url)
        data = yaml.load(response.content)
        repos = {}
        for arg in data:
            repos[arg['name']] = {'is_private':
                                  arg['is_private'],
                                  'state': arg['state'],
                                  'scm': arg['scm']}
        return repos
