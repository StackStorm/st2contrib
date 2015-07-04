from lib.action import TravisCI


class RestartBuildAction(TravisCI):
    def run(self, buildid):
        """
        Restart a build by providing it's id
        """
        uri = self.config["uri"] + '/builds/' + str(buildid) + '/restart'
        response = self._perform_request(uri, method="POST")
        return response.content
