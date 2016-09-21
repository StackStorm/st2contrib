
from lib.base import BaseGithubAction


class ListReleasesAction(BaseGithubAction):
    def run(self, api_user, repository):
        results = []

        if api_user:
            self.token = self._get_user_token(api_user)

        releases = self._request("GET",
                                 "/repos/{}/releases".format(repository),
                                 None,
                                 self.token)

        for release in releases:
            results.append(
                {'author': release['author']['login'],
                 'html_url': release['html_url'],
                 'tag_name': release['tag_name'],
                 'target_commitish': release['target_commitish'],
                 'name': release['name'],
                 'body': release['body'],
                 'draft': release['draft'],
                 'prerelease': release['prerelease'],
                 'created_at': release['created_at'],
                 'published_at': release['published_at'],
                 'total_assets': len(release['assets'])})

        return results
