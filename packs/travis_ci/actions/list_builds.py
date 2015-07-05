from lib.action import TravisCI


class ListBuildsAction(TravisCI):
    def run(self, repo_name, username):
        """
        Listing builds for a give Repository
        """
        path = '/repos/' + username + '/' + repo_name + '/builds'
        response = self._perform_request(path, method='GET')
        data = response.json()
        return data
