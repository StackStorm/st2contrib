
import time
import datetime

from lib.base import BaseGithubAction


class CreateReleaseAction(BaseGithubAction):
    def run(self, api_user, repository, name, body, github_type,
            target_commitish="master", version_increase="patch",
            draft=False, prerelease=False):

        enterprise = self._is_enterprise(github_type)

        if api_user:
            self.token = self._get_user_token(api_user,
                                              enterprise)

        release = self._request("GET",
                                "/repos/{}/releases/latest".format(repository),
                                None,
                                self.token,
                                enterprise)

        (major, minor, patch) = release['tag_name'].split(".")
        major = int(major.replace("v", ""))
        minor = int(minor)
        patch = int(patch)

        if version_increase == "major":
            major += 1
            minor = 0
            patch = 0
        elif version_increase == "minor":
            minor += 1
            patch = 0
        elif version_increase == "patch":
            patch += 1

        tag_name = "v{}.{}.{}".format(major,
                                      minor,
                                      patch)

        payload = {"tag_name": tag_name,
                   "target_commitish": target_commitish,
                   "name": name,
                   "body": body,
                   "draft": draft,
                   "prerelease": prerelease}

        release = self._request("POST",
                                "/repos/{}/releases".format(repository),
                                payload,
                                self.token,
                                enterprise)

        ts_published_at = time.mktime(
            datetime.datetime.strptime(
                release['published_at'],
                "%Y-%m-%dT%H:%M:%SZ").timetuple())

        results = {'author': release['author']['login'],
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
        results['response'] = release

        return results
