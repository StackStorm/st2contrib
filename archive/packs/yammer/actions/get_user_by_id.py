from lib.actions import YammerAction

__all__ = [
    'GetUserByIdAction'
]


class GetUserByIdAction(YammerAction):
    def run(self, id=None):
        yammer = self.authenticate()
        user = yammer.users.find(id)
        return user
