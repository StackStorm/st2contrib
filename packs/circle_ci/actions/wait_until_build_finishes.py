import httplib
import time

from lib.action import CircleCI


class WaitUntilBuildFinishes(CircleCI):

    def run(self, build_number, project, wait_timeout=600):
        """
        Get build number for a SHA in project.
        """
        path = 'project/%s/%s' % (project, build_number)

        start_time = time.time()
        done = False
        while not done:
            response = self._perform_request(
                path, method='GET',
            )

            if response.status_code != httplib.OK:
                msg = ('Build number %s for project ' % build_number +
                       '%s not found.' % project)
                raise Exception(msg)

            response = response.json()

            if response['lifecycle'] == 'finished':
                return True

            time.sleep(10)
            done = (time.time() - start_time) > wait_timeout

        return False
