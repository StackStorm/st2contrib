import httplib

from lib.action import CircleCI


class GetBuildNumberAction(CircleCI):

    def run(self, vcs_revision, project, search_limit=10):
        """
        Get build number for a SHA in project.
        """
        path = 'project/' + project

        response = self._perform_request(
            path, method='GET',
            extra_headers={'limit': int(search_limit)}
        )

        if response.status_code != httplib.OK:
            raise Exception('Project %s not found.' % project)

        for build in response.json:
            if build['vcs_revision'] == vcs_revision:
                return build['build_number']
