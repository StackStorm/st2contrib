from lib.base import BaseGithubAction
from github import GithubObject
from lib.formatters import issue_to_dict

__all__ = [
    'CreateIssueAction'
]


class CreateIssueAction(BaseGithubAction):
    def run(self, user, repo, title, description=None, assignee=None):
        user = self._client.get_user(user)
        repo = user.get_repo(repo)
        issue = repo.create_issue(title, description or GithubObject.NotSet,
                                  assignee or GithubObject.NotSet)
        result = issue_to_dict(issue=issue)
        return result
