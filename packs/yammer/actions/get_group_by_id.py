from lib.actions import YammerAction

__all__ = [
    'GetGroupByIdAction'
]


class GetGroupByIdAction(YammerAction):
    def run(self, id=None):
        yammer = self.authenticate()
        user = yammer.groups.find(id)
        return user
