import httplib
import json

from lib.action import CircleCI


class RunBuild(CircleCI):

    def run(self, project, branch=None, tag=None, vcs_revision=None):
        """
        Run build for a SHA in project.
        """

        # Add some explicit mutually-exclusive checks.
        if not(branch or tag or vcs_revision):
            raise Exception('At least one of branch, tag or vcs_revision should be provided.')
        if (branch and (tag or vcs_revision)) or (tag and vcs_revision):
            raise Exception('Only one of branch, tag or vcs_revision should be provided.')

        data = None
        if branch:
            path = 'project/%s/tree/%s' % (project, branch)
        else:
            path = 'project/%s' % project
            data = {'tag': tag} if tag else {'revision': vcs_revision}
            data = json.dumps(data)

        response = self._perform_request(path, method='POST', data=data)

        if response.status_code != httplib.CREATED:
            message = response.json().get('message', 'Unknown reason.')
            raise Exception('Failed to run build : %s' % message)

        return response.json()
