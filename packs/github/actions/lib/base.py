from github import Github

from st2actions.runners.pythonrunner import Action

__all__ = [
    'BaseGithubAction'
]


class BaseGithubAction(Action):
    def __init__(self, config):
        super(BaseGithubAction, self).__init__(config=config)
        self._client = Github(self.config['token'])
