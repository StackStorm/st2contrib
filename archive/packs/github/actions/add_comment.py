from lib.base import BaseGithubAction

__all__ = [
    'AddCommentAction'
]


class AddCommentAction(BaseGithubAction):
    def run(self, user, repo, issue, body):
        issue = int(issue)

        user = self._client.get_user(user)
        repo = user.get_repo(repo)
        issue = repo.get_issue(issue)

        issue.create_comment(body=body)
        return True
