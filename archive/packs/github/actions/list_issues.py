import datetime

from lib.base import BaseGithubAction
from lib.formatters import issue_to_dict

__all__ = [
    'ListIssuesAction'
]


class ListIssuesAction(BaseGithubAction):
    def run(self, user, repo, filter=None, state=None, sort=None,
            direction=None, since=None, limit=20):
        user = self._client.get_user(user)
        repo = user.get_repo(repo)

        kwargs = {}
        if filter:
            kwargs['filter'] = filter
        if state:
            kwargs['state'] = state
        if sort:
            kwargs['sort'] = sort
        if direction:
            kwargs['direction'] = direction
        if since:
            kwargs['since'] = datetime.datetime.fromtimestamp(since)

        # Note: PyGithub library introduces an abstraction for paginated lists
        # which doesn't conform to Python's iterator spec so we can't use
        # array slicing to exhaust the list :/
        issues = repo.get_issues(**kwargs)
        issues = list(issues)

        result = []
        for index, issue in enumerate(issues):
            issue = issue_to_dict(issue=issue)
            result.append(issue)

            if (index + 1) >= limit:
                break

        return result
