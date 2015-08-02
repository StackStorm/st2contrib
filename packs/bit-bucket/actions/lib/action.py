from st2actions.runners.pythonrunner import Action
from bitbucket.bitbucket import Bitbucket


class BitBucketAction(Action):
    def __init__(self, config):
        super(BitBucketAction, self).__init__(config)

    def perform_request(self, repo=''):
        if repo:
            bb = Bitbucket(username=self.config['username'],
                           password=self.config['password'],
                           repo_name_or_slug=repo)
        else:
            bb = Bitbucket(username=self.config['useremail'],
                           password=self.config['password'])
        return bb
