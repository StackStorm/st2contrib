import httplib

from lib.action import CircleCI


class RunBuild(CircleCI):

    def run(self, project, branch):
        """
        Run build for a SHA in project.
        """
        path = 'project/%s/tree/%s' % (project, branch)

        response = self._perform_request(
            path, method='POST'
        )

        if response.status_code != httplib.CREATED:
            raise Exception('Project %s not found.' % project)

        return response.json()
