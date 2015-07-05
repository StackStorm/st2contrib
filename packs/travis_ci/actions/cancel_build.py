from lib.action import TravisCI


class CancelBuildAction(TravisCI):
    def run(self, build_id):
        """
        Cancel a build by providing it's id
        """
        path = '/builds/' + str(build_id) + '/cancel'
        response = self._perform_request(path, method='POST')
        return response.content
