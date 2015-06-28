from lib.base import BaseGithubAction

__all__ = [
    'GetTrafficStatsAction'
]


class GetTrafficStatsAction(BaseGithubAction):
    def run(self, repo):
        traffic_data = self._get_analytics(category='traffic-data', repo=repo)
        return traffic_data['summary']
