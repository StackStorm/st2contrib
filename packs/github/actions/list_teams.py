from lib.base import BaseGithubAction
from lib.formatters import team_to_dict

__all__ = [
    ListTeamsAction'
]


class ListTeamsAction(BaseGithubAction):
    def run(self, organization):
        organization = self._client.get_organization(organization)
        teams = organization.get_teams()
        result = []
        for team in enumerate(teams):
            team = team_to_dict(team=team)
            result.append(team)

        return result
