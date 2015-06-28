from st2actions.runners.pythonrunner import Action
import requests


class BitBucket(Action):
    def __init__(self, config):
        super(BitBucket, self).__init__(config)

    def _perform_request(self, url, method=None, query_params=None):
        return requests.get(url, auth=(self.config['useremail'],
                                       self.config['password']))
