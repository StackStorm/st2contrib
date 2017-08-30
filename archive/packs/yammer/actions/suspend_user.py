from lib.actions import YammerAction

__all__ = [
    'SuspendUserAction'
]


class SuspendUserAction(YammerAction):
    def run(self, id=None):
        yammer = self.authenticate()
        user = yammer.users.suspend(id)
        return user
