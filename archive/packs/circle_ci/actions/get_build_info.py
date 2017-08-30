import httplib

from lib.action import CircleCI


class GetBuildInfoAction(CircleCI):

    def run(self, project, build_num):
        """
        Get build number for a SHA in project.
        """
        path = 'project/%s/%s' % (project, build_num)

        response = self._perform_request(
            path, method='GET'
        )

        if response.status_code != httplib.OK:
            raise Exception('Build %s of project %s not found.' % (build_num, project))

        return response.json()
