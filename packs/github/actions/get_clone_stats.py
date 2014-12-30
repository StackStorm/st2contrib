from lib.base import BaseGithubAction

__all__ = [
    'GetCloneStatsAction'
]

class GetCloneStatsAction(BaseGithubAction):
    def run(self, repo):
        clone_data = self._get_analytics(category='clone-activity-data', repo=repo)
        return clone_data['summary']

