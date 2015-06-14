from lib.action import TravisCI
import requests


class BuildRepo(TravisCI):
    def run(self, buildid, action):
        """
        Restart a build or Cancel a build by providing it's id
        """
        _HEADERS = self.travis
        _HEADERS['Authorization'] = self.config["Authorization"]
        _HEADERS['Content-Type'] = self.config["Content-Type"]
        uri = self.config["uri"] + '/builds/' + str(buildid) + '/' + action
        response = requests.post(uri, headers=_HEADERS)
        return response.content
