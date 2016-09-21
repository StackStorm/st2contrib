
import time
import datetime

from lib.base import BaseGithubAction


class LatestReleaseAction(BaseGithubAction):
    def run(self, api_user, repository):

        if api_user:
            self.token = self._get_user_token(api_user)

        release = self._request("GET",
                                "/repos/{}/releases/latest".format(repository),
                                None,
                                self.token)

        ts_published_at = time.mktime(
            datetime.datetime.strptime(
                release['published_at'],
                "%Y-%m-%dT%H:%M:%SZ").timetuple())

        results = {'author': release['author']['login'],
                   'avatar_url': release['author']['avatar_url'],
                   'html_url': release['html_url'],
                   'tag_name': release['tag_name'],
                   'target_commitish': release['target_commitish'],
                   'name': release['name'],
                   'body': release['body'],
                   'draft': release['draft'],
                   'prerelease': release['prerelease'],
                   'created_at': release['created_at'],
                   'published_at': release['published_at'],
                   'ts_published_at': ts_published_at,
                   'total_assets': len(release['assets'])}

        return results
