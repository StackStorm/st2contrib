from lib.action import TravisCI


class CancelBuildAction(TravisCI):
    def run(self, buildid):
        """
        Cancel a build by providing it's id
        """
        path = '/builds/' + str(buildid) + '/cancel'
        response = self._perform_request(path, method="POST")
        return response.content
