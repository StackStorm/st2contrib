from lib.base import BaseGithubAction
from lib.formatters import user_to_dict

__all__ = [
    'AddTeamMembershipAction'
]


class AddTeamMembershipAction(BaseGithubAction):
    def run(self, team, user):
        user = self._client.get_user(user)
        organization = self._client.get_organization(self.config.user)
        team = organization.get_team(team)
        team.add_membership(member=user)
        result = user_to_dict(user=user)
        return result
