from lib.action import TravisCI


class RestartBuildAction(TravisCI):
    def run(self, buildid):
        """
        Restart a build by providing it's id
        """
        path = '/builds/' + str(buildid) + '/restart'
        response = self._perform_request(path, method='POST')
        return response.content
