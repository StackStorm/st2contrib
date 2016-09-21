from lib.base import BaseGithubAction


class StoreOauthToken(BaseGithubAction):
    def run(self, user, token, enterprise=False):

        if enterprise:
            value_name = "token_enterprise_{}".format(user)
        else:
            value_name = "token_{}".format(user)

        self.action_service.set_value(
            name=value_name,
            value=token)

        return True
