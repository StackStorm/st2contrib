from lib.action import TravisCI
import requests


class BuildRepo(TravisCI):
    def run(self, buildid, action):
        """
        Restart a build or Cancel a build by providing it's id
        """
        uri = self.config["uri"]+'/builds/'+str(buildid)+'/'+action
        response = self._perform_request(uri, method="POST")
        return response.content
