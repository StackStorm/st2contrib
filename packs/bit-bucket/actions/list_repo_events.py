#from lib.action import BitBucket
import yaml
from bitbucket.bitbucket import Bitbucket

class ListRepoEventsAction():
    def run(self):
        """
        List events performed on a repository
        """
        bb = Bitbucket("razaaamir", "amadraza@512", "testss")
        a,v=bb.repository.all()
        for i in v:
            print "================, ", v
       # url = self.config['Host']+'repositories/' + \
       #     self.config['username'] + '/' + repo + '/events/'
       # response = self._perform_request(url)
       # data = yaml.load(response.content)
       # res = []
       # for i in range(data['count']):
       #     if data['events'][i]['event'] != 'create':
       #         res.append({data['events'][i]['event']:
       #                    {'total_commits': data['events'][i]
       #                    ['description']['total_commits']}})
     

if __name__ == "__main__":
    c=ListRepoEventsAction()
    c.run()  
