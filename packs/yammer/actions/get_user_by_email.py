from lib.actions import YammerAction

__all__ = [
    'GetUserByEmailAction'
]


class GetUserByEmailAction(YammerAction):
    def run(self, email=None):
        yammer = self.authenticate()
        user = yammer.users.find_by_email(email)
        return user
