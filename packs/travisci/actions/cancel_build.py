from lib.action import TravisCI


class CancelBuildAction(TravisCI):
    def run(self, buildid):
        """
        Cancel a build by providing it's id
        """
        uri = self.config["uri"] + '/builds/' + str(buildid) + '/cancel'
        response = self._perform_request(uri, method="POST")
        return response.content
