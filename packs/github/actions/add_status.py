from github import GithubObject

from lib.base import BaseGithubAction

__all__ = [
    'AddCommitStatusAction'
]


class AddCommitStatusAction(BaseGithubAction):
    def run(self, user, repo, sha, state, target_url=None, description=None):
        target_url = target_url or GithubObject.NotSet
        description = description or GithubObject.NotSet

        user = self._client.get_user(user)
        repo = user.get_repo(repo)
        commit = repo.get_commit(sha)

        commit.create_status(state=state, target_url=target_url,
                             description=description)
        return True
