from lib.action import BitBucket
import yaml


class ListBrachesAction(BitBucket):
    def run(self, repo):
        """
        List Braches of Repository with author names and message
        """
        url = self.config['Host'] + 'repositories/' + \
            self.config['username'] + '/' + repo + '/branches/'
        response = self._perform_request(url)
        data = yaml.load(response.content)
        res = []
        for k, v in data.iteritems():
            res.append({v['branch']: {'author': v['author'],
                       'message': v['message']}})
        return res
