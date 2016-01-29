from lib.base import BaseGithubAction
from lib.formatters import user_to_dict

__all__ = [
    'GetUserAction'
]


class GetUserAction(BaseGithubAction):
    def run(self, user):
        user = self._client.get_user(user)
        result = user_to_dict(user=user)
        return result
