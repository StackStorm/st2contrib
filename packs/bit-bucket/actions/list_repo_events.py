from lib.action import BitBucket
import yaml


class ListRepoEventsAction(BitBucket):
    def run(self, repo):
        """
        List events performed on a repository
        """
        url = self.config['Host']+'repositories/' + \
            self.config['username'] + '/' + repo + '/events/'
        response = self._perform_request(url)
        data = yaml.load(response.content)
        res = []
        for i in range(data['count']):
            if data['events'][i]['event'] != 'create':
                res.append({data['events'][i]['event']:
                           {'total_commits': data['events'][i]
                           ['description']['total_commits']}})
        return res
