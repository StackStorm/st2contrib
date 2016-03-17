import httplib

from lib.action import CircleCI


class RetryBuild(CircleCI):

    def run(self, project, build_num):
        """
        ReRun a specific build in project.
        """
        path = 'project/%s/%s/retry' % (project, build_num)

        response = self._perform_request(
            path, method='POST'
        )

        if response.status_code != httplib.CREATED:
            raise Exception('Project %s not found.' % project)

        return response.json()
