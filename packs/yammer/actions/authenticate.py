from lib.actions import YammerAction

__all__ = [
    'AuthenticateAction'
]


class AuthenticateAction(YammerAction):
    def run(self):
        auth_url = self.authenticator.authorization_url(
            redirect_uri=self.expected_redirect)
        return {"url": auth_url}
