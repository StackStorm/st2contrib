from lib.base import BaseGithubAction
from lib.formatters import issue_to_dict

__all__ = [
    'GetIssueAction'
]


class GetIssueAction(BaseGithubAction):
    def run(self, user, repo, issue_id):
        issue_id = int(issue_id)

        user = self._client.get_user(user)
        repo = user.get_repo(repo)
        issue = repo.get_issue(issue_id)
        result = issue_to_dict(issue=issue)
        return result
